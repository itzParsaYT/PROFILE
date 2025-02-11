from django.db import models


# Create your models here.

class Key(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    anthropic_api_key = models.CharField(max_length=300, null=True, blank=True)
    aws_access_key_id = models.CharField(max_length=300, null=True, blank=True)
    aws_secret_key = models.CharField(max_length=300, null=True, blank=True)
    aws_region = models.CharField(max_length=300, null=True, blank=True)
    azure_openai_key = models.CharField(max_length=300, null=True, blank=True)
    azure_endpoint_url = models.CharField(max_length=300, null=True, blank=True)
    azure_deployment_name = models.CharField(max_length=300, null=True, blank=True)



    def __str__(self):
        return f"{self.name}"


class Agent(models.Model):
    name = models.CharField(max_length=100,default="no_name")
    company_objective = models.CharField(max_length=200)
    company_url = models.CharField(max_length=200, null=True)
    job = models.CharField(max_length=100, default='no_job')
    memory = models.BooleanField(default=False)
    compress = models.BooleanField(default=False)
    irrelevant = models.BooleanField(default=False)
    api_key = models.ForeignKey(Key, on_delete=models.CASCADE)
    LLM = models.CharField(max_length=200,default="gpt-4o")


    def __str__(self):
        return f"{self.name}"


class Task(models.Model):
    text = models.TextField()
    multi_process = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    task_attachment = models.FileField(upload_to="task_attachments", null=True, blank=True)
    agents = models.ManyToManyField('Agent', related_name="tasks")
    done = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text[:35]}"


class Answer(models.Model):
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    task = models.OneToOneField(Task, on_delete=models.CASCADE, blank=True, null=True, related_name="answer")


    def __str__(self):
        return f"{self.task.agents.all()} | {self.text[:20]}"

    def save(self, *args, **kwargs):
        # Ensure that the agents field is set to the agents of the connected task
        if self.task:
            self.agents.set(self.task.agents.all())
        super().save(*args, **kwargs)


class profile(models.Model):
    name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    gmail = models.CharField(max_length=100, null=True)
