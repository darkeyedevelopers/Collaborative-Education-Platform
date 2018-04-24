# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import classrooms,snippets,lectures,vote_classroom
# Register your models here.
admin.site.register(classrooms)
admin.site.register(snippets)

admin.site.register(lectures)
admin.site.register(vote_classroom)
