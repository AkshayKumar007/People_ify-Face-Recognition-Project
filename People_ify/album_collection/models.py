from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Person_Group(models.Model):
    pg_id = models.AutoField(primary_key=True)
    pg_name = models.CharField(max_length=128)

class Person_Group_Person(models.Model):
    class Meta:
        unique_together = (('pgp_id', 'pg_id'),)
    pgp_id = models.AutoField(primary_key=True)
    pg_id = models.ForeignKey(Person_Group, on_delete=models.CASCADE)
    pgp_name = models.CharField(max_length=128)
    person_id = models.CharField(max_length=128)

class FolderName(models.Model):
    f_id = models.AutoField(primary_key=True)
    pg_id = models.ForeignKey(Person_Group, on_delete=models.CASCADE)
    pgp_id = models.ForeignKey(Person_Group_Person, on_delete=models.CASCADE)
    folder_name = models.CharField(max_length=128, unique=True)
    folder_path = models.TextField()

class Review(models.Model):
    class Meta:
        unique_together = (('rev_id','pg_id'),)
    rev_id = models.AutoField(primary_key=True)
    pg_id = models.ForeignKey(Person_Group, on_delete=models.CASCADE)
    review = models.TextField()
    rev_star = models.IntegerField()
    # def __str__(self):
    #     return "{0}\t{1}\n{2}\n{3}".format(self.rev_id, self.pg_id, self.rev_star, self.review)

# class sharedFolder(models.Model):
#     pg_id1 = models.ForeignKey(FolderName, on_delete=models.CASCADE, related_name="from")
#     f_id = models.ForeignKey(FolderName, on_delete=models.CASCADE)
#     pg_id2 = models.ForeignKey(Person_Group, on_delete=models.CASCADE, related_name="to")
    
    