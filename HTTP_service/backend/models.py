from django.db import models


class User(models.Model):
    name = models.CharField(max_length=20, unique=True)


class FileU(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="file")
    created_data = models.DateTimeField(auto_now_add=True)
    column_file = models.TextField()
    file = models.FileField()
