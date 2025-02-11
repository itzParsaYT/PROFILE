from django import forms
from .models import Key

all_llm_types = {
    "claude-v1",
    "claude-v2",
    "claude-instant-v1"
    ,
    "amazon.titan-tg1-large",
    "ai21.j2-mid",
    "ai21.j2-ultra",
    "cohere.command-text-v14"
    ,
    "gpt-3.5-turbo",
    "gpt-4",
    "gpt-4-32k",
    "text-davinci-003",
    "code-davinci-002",
    "text-curie-001",
    "text-babbage-001",
    "text-ada-001"

}



class AgentForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        keys = Key.objects.all()
        self.fields['api_key'].choices = [('', 'choose your key')] + [(key.id, key.name) for key in keys]
        self.fields['LLM'].choices = [('', 'choose your LLM')] + [(llm,llm) for llm in all_llm_types]

    # Text Input Fields
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'textInput',
            'placeholder': 'name',
        }),
        required=True
    )

    LLM = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'text-xs outline-0 focus:outline-0 min-h-max max-h-min w-48',
        }),
        choices=[],  # Will be populated in __init__
        required=True
    )

    job = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'textInput',
            'placeholder': 'job title',
        }),
        required=True
    )

    company_url = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'textInput',
            'placeholder': 'company url',
        }),
        required=True
    )

    company_objective = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'textInput',
            'placeholder': 'company objective',
        }),
        required=True
    )

    memory = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'hidden-checkbox',
        })
    )

    compress = forms.BooleanField(
        required=False,
        label="I agree to the terms and conditions",
        widget=forms.CheckboxInput(attrs={
            'class': 'hidden-checkbox',
        })
    )

    irrelevant = forms.BooleanField(
        required=False,
        label="I agree to the terms and conditions",
        widget=forms.CheckboxInput(attrs={
            'class': 'hidden-checkbox',
        })
    )

    # Select Dropdown
    api_key = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'text-xs outline-0 focus:outline-0 min-h-max max-h-min w-48',
        }),
        choices=[],

    )






class AnthropicForm(forms.Form):
    anthropic_api_key = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'textInput',
            'placeholder': 'Anthropic API Key',
            'id': 'id_anthropic_api_key'
        }),
        required=True
    )


class BedrockForm(forms.Form):
    aws_access_key_id = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'textInput',
            'placeholder': 'AWS Access Key ID',
            'id': 'id_aws_access_key'
        }),
        required=True
    )

    aws_secret_key = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'textInput',
            'placeholder': 'AWS Secret Access Key',
            'id': 'id_aws_secret'
        }),
        required=True
    )

    aws_region = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'textInput',
            'placeholder': 'AWS Region (e.g., us-east-1)',
            'id': 'id_aws_region'
        }),
        required=True
    )


class AzureForm(forms.Form):
    azure_openai_key = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'textInput',
            'placeholder': 'Azure OpenAI Key',
            'id': 'id_azure_key'
        }),
        required=True
    )

    azure_endpoint = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'textInput',
            'placeholder': 'Azure Endpoint URL',
            'id': 'id_azure_endpoint'
        }),
        required=True
    )

    azure_deployment = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'textInput',
            'placeholder': 'Deployment Name (e.g., gpt-4)',
            'id': 'id_azure_deployment'
        }),
        required=True
    )