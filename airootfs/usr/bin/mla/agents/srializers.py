from rest_framework import serializers

from agents.models import Agent, Task, Key


class AgentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Agent
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class KeySerializer(serializers.ModelSerializer):
    class Meta:
        model = Key
        fields = '__all__'