from django.db import models

# Create your models here.
class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64,null=False,unique=True)
    publisher = models.ForeignKey(to="publisher.Publisher")