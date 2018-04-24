# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class classrooms(models.Model):
    class_name = models.CharField(max_length=100)
    course_name = models.CharField(max_length=100)
    desc = models.TextField()
    start_time = models.DateField()
    end_time = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upvote_cnt = models.IntegerField()
    downvote_cnt = models.IntegerField()

class vote_classroom(models.Model):
    classroom = models.ForeignKey(classrooms, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_type = models.BooleanField()

class lectures(models.Model):
    lecture_name = models.CharField(max_length=100)
    classroom = models.ForeignKey(classrooms, on_delete=models.CASCADE)
    lecture_url = models.URLField()
    start_time = models.DateField()
    end_time = models.DateField()
    trans_script = models.TextField()

class snippets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    c_code = models.TextField()
    html = models.TextField()
    cpp_code = models.TextField()
    java_code = models.TextField()
    py_code = models.TextField()
    py3_code = models.TextField()
    result = models.TextField()
    desc = models.TextField()
