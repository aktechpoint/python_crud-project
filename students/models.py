from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=13)
    address = models.TextField()

    def __str__(self):
        return self.name
