from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Person_Group(models.Model):
    pg_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=128)


class Person_Group_Person(models.Model):
    pgp_id = models.IntegerField(primary_key=True)
    pg_id = models.ForeignKey(Person_Group, on_delete=models.CASCADE)

class FolderName(models.Model):
    pg_id = models.ForeignKey(Person_Group, on_delete=models.CASCADE)
    pgp_id = models.ForeignKey(Person_Group_Person, on_delete=models.CASCADE)
    folder_name = models.CharField(max_length=128)
    folder_path = models.CharField(max_length=128)

class sharedFolder(models.Model):
    pg_id1 = models.ForeignKey(Person_Group, on_delete=models.CASCADE)
    pg_id2 = models.ForeignKey(Person_Group, on_delete=models.CASCADE)
    