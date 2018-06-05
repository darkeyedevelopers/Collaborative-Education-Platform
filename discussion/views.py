from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from dashboard.models import classrooms
import datetime
from .models import Discussion
from django.apps import apps

from channels import Group
import json


def disc(request,class_name):
	
	print ('In disc'+class_name)	
	classroom=classrooms.objects.get(class_name=class_name)
	user=request.user
	return render(request,'discussion/forum.html',{'All':Discussion.objects.filter(classroom=classroom),'class_name':class_name})


def addcom(request):
	print ('In addcom')
	user=request.user
	class_name = request.POST.get('class_name')
	classroom=classrooms.objects.get(class_name=class_name)
	message = request.POST.get('comment')
	
	time = datetime.datetime.now().replace(microsecond=0)
	
	discussion = Discussion(user=user,classroom=classroom,message=message,time=time)
	discussion.save()
	class_name=class_name.replace(" ","_")
	text={'text1': '<div class="comment"><div class="content"><a class="author">'+str(discussion.user.username)+'</a><div class="metadata"><div class="date">'+str(discussion.time)+'</div></div><pre class="ui segment" style="background-color: #f8f8f8;border:0px;">'+str(discussion.message)+'</pre></div></div>','text2': '<div class="comment"><div class="content"><a class="author">'+str(discussion.user.username)+'</a><div class="metadata"><div class="date">'+str(discussion.time)+'<button class="ui mini button" onclick="delete_com('+str(discussion.id) +')">DELETE</button></div></div><pre class="ui segment" style="background-color: #f8f8f8;border:0px;">'+str(discussion.message)+'</pre></div></div>','username':str(user.username)}
	Group(class_name).send({'text':json.dumps(text)})
	return HttpResponse("success")


def delcom(request):
	com=request.POST.get('com')
	Discussion.objects.filter(id=com).delete()
	return HttpResponse("success")




