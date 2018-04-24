# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Roadmap(models.Model):
    r_title=models.CharField(max_length=50)
    r_descri = models.CharField(max_length=50)
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    upcount = models.IntegerField(default=0)
    downcount = models.IntegerField(default=0)
    published_date= models.DateTimeField(blank=True)
    def __str__(self):
        return ""+self.r_title

class Step(models.Model):
    roadmap=models.ForeignKey(Roadmap,on_delete=models.CASCADE)
    seq_no=models.IntegerField()
    step_name=models.CharField(max_length=50)
    step_descri = models.CharField(max_length=200)
    duration=models.IntegerField(blank=True)
    def __str__(self):
        return ""+self.step_name


class Resource(models.Model):
    step=models.ForeignKey(Step,on_delete=models.CASCADE)
    roadmap=models.ForeignKey(Roadmap,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    link=models.CharField(max_length=50)
    def __str__(self):
        return ""+self.name

class Upvote(models.Model):
    roadmap=models.ForeignKey(Roadmap,on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return ""+self.roadmap.r_title+" "+self.user

class Downvote(models.Model):
    roadmap=models.ForeignKey(Roadmap,on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return ""+self.roadmap.r_title+" "+self.user
