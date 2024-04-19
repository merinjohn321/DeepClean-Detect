from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Registration(models.Model):
    name=models.CharField(max_length=20)
    email=models.CharField(max_length=20)
    address=models.CharField(max_length=100)
    phone=models.BigIntegerField()
    idproof = models.FileField(upload_to='proofs')
    age=models.IntegerField()
    totalpoint = models.IntegerField(null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)

class Detections(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    image = models.FileField(upload_to='detections')
    results = models.CharField(max_length=200,null=True)
    Registration=models.ForeignKey(Registration,on_delete=models.CASCADE)

class Points(models.Model):
    date = models.DateField(auto_now_add=True)
    Detections = models.ForeignKey(Detections, on_delete=models.CASCADE)
    Registration=models.ForeignKey(Registration,on_delete=models.CASCADE)
    point = models.IntegerField()