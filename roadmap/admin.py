# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Roadmap,Step,Resource
from django.contrib import admin

# Register your models here.
admin.site.register(Roadmap)
admin.site.register(Step)
admin.site.register(Resource)
