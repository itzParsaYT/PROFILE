from django.db import models

# Create your models here.


class UserProfile(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=60)
    lastname = models.CharField(max_length=40)
    gmail = models.CharField(max_length=50)

    def __str__(self):
        return self.username
    