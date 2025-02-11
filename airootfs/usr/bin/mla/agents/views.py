from asyncio import all_tasks
from os.path import split
from tkinter.font import names

from django.core.serializers import serialize
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .forms import AgentForm, BedrockForm, AzureForm, AnthropicForm
from .models import Agent, Key, Answer,Task
from .srializers import AgentSerializer, TaskSerializer, KeySerializer
from upsonic import UpsonicClient, ObjectResponse, Task as UpsonicTask, AgentConfiguration
from upsonic.client.tools import Search


# Create your views here.

def dashboard(request):
    all_ai_types = {
        "anthropic": [
            "claude-v1",
            "claude-v2",
            "claude-instant-v1"
        ],
        "bedrock": [
            "amazon.titan-tg1-large",
            "ai21.j2-mid",
            "ai21.j2-ultra",
            "cohere.command-text-v14"
        ],
        "azure": [
            "gpt-3.5-turbo",
            "gpt-4",
            "gpt-4-32k",
            "text-davinci-003",
            "code-davinci-002",
            "text-curie-001",
            "text-babbage-001",
            "text-ada-001"
        ]
    }
    agents = Agent.objects.all()

    if request.method == 'GET':
        return render(request, "agents/dashboasrd.html",
                      context={'all_ai_types': all_ai_types, "agents": agents, "keys": Key.objects.all(),
                               'form': AgentForm(), "created": True, 'anthropic_form': AnthropicForm(),
                               'bedrock_form': BedrockForm(),
                               'azure_form': AzureForm()})

    if request.method == 'POST':

        form = AgentForm(request.POST)
        if form.is_valid():
            # Process validated data
            data = form.cleaned_data
            for key in Key.objects.all():
                for type, value in all_ai_types:
                    if key.company == type:
                        for llm in value:
                            if llm == data['LLM']:
                                data['api_key'] = key.api_key
                                Agent.objects.create(**data)
                                return render(request, "agents/dashboasrd.html",
                                              context={'all_ai_types': all_ai_types, "agents": agents,
                                                       "keys": Key.objects.all(), 'form': form, 'created': True,
                                                       'anthropic_form': AnthropicForm(),
                                                       'bedrock_form': BedrockForm(),
                                                       'azure_form': AzureForm()
                                                       })

            return render(request, "agents/dashboasrd.html",
                          context={'all_ai_types': all_ai_types, "agents": agents, "keys": Key.objects.all(),
                                   'form': form, 'created': False, 'anthropic_form': AnthropicForm(),
                                   'bedrock_form': BedrockForm(),
                                   'azure_form': AzureForm()
                                   })

    else:

        form = AgentForm()
    return render(request, "agents/dashboasrd.html",
                  context={'all_ai_types': all_ai_types, "agents": agents, "keys": Key.objects.all(), 'form': form,
                           "created": True, 'anthropic_form': AnthropicForm(),
                           'bedrock_form': BedrockForm(),
                           'azure_form': AzureForm()
                           })


def talk(request):
    tasks = Task.objects.all()
    answers = Answer.objects.all()
    agents = Agent.objects.all()
    return render(request, "agents/index.html", context={"tasks": tasks, "answers": answers, "agents": agents})


class KeyViewSet(viewsets.ViewSet):

    def create(self, request):
        serializer = KeySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskViewSet(viewsets.ViewSet):

    def create(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            upsonic_run(serializer.validated_data,Task.objects.all().last())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        serializer = TaskSerializer(Task.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        serializer = TaskSerializer(Task.objects.get(pk=pk))
        return Response(serializer.data)


class AgentViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = AgentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnswerViewSet(viewsets.ViewSet):
    def list(self, request):
        answers = Answer.objects.all()
        return Response(answers, status=status.HTTP_200_OK)



def upsonic_run(data,task):
    client = UpsonicClient("localserver")

    client.default_llm_model = data["agents"][0].LLM

    api_key = Key.objects.get(pk=data['agents'][0].api_key.id)


    if (api_key.company == "anthropic"):
        client.set_config("ANTHROPIC_API_KEY", api_key.anthropic_api_key)
    elif(api_key.company == "azure"):
        client.set_config("AZURE_OPENAI_ENDPOINT", api_key.azure_endpoint_url)
        client.set_config("AZURE_OPENAI_API_KEY", api_key.azure_openai_key)
    else:
        client.set_config("AWS_ACCESS_KEY_ID", api_key.aws_access_key_id)
        client.set_config("AWS_SECRET_ACCESS_KEY", api_key.aws_secret_key)
        client.set_config("AWS_REGION", api_key.aws_region)

    # Create an Upsonic client instance

    agent = AgentConfiguration(
        agent_id_=data['agents'][0].id,
        memory=data['agents'][0].memory,
        name=data['agents'][0].name,
        compress_context=data['agents'][0].compress,
        job_title=data['agents'][0].job,
        company_url=data['agents'][0].company_url,
        company_objective=data['agents'][0].company_objective,

    )

    description_of_task = data["text"]

    class TaskAnswer(ObjectResponse):
        title: str
        body: str
        url: str
        tags: list[str]

    class ResponseFormat(ObjectResponse):
        _list: list[TaskAnswer]


    task1 = UpsonicTask(description=description_of_task, response_format=ResponseFormat)
    client.agent(agent,task1)

    Answer.objects.create(task=task,text=task1.response)

    return task1.response
