from django.contrib import admin
from .models import Agent,  Task, Answer, Key
# Register your models here.


admin.site.register(Agent)
admin.site.register(Task)
admin.site.register(Answer)
admin.site.register(Key)
