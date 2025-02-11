from django.http import HttpResponse
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Agent, dashboard, talk, TaskViewSet, KeyViewSet, AgentViewSet, AnswerViewSet

urlpatterns = [
    path('task/create/', TaskViewSet.as_view({'post': 'create'}), name='task-create'),
    path('task/list/', TaskViewSet.as_view({'get': 'list'}), name='task-list'),
    path('task/retrieve/', TaskViewSet.as_view({'get': 'retrieve'}), name='task-retrieve'),
    path("dashboard/", dashboard, name='dashboard'),
    path("talk/", talk, name='talk'),
    path("apikey/create/", KeyViewSet.as_view({'post': 'create'}), name='apikey-create'),
    path("create/", AgentViewSet.as_view({'post': 'create'}), name='agent-create'),
    path("answer/list/", AnswerViewSet.as_view({'get': 'list'}), name='answer-list'),
]
