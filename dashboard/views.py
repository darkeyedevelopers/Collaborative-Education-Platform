# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import classrooms,snippets,lectures,vote_classroom
from django.http import HttpResponse
from django.contrib.auth.models import User
import json
# Create your views here.

def index(request):
    classes = classrooms.objects.all()
    return render(request,'dashboard.html',{'classrooms':classes})

def tocreateroom(request):
    return render(request,'createclassroom.html')

def createroom(request):
    c_name = request.POST.get('class_name')
    course_name = request.POST.get('course_name')
    desc = request.POST.get('desc')
    start = request.POST.get('start')
    end = request.POST.get('end')
    user = User.objects.get(username=request.user.username)
    new_classroom = classrooms(user=user,start_time=start,end_time=end,class_name = c_name,course_name=course_name,desc=desc,upvote_cnt=0,downvote_cnt=0)
    new_classroom.save()
    return HttpResponse('success')

def toaddlecture(request):
    return render(request,'addLecture.html')

def addlecture(request):
    name = request.POST.get('lecture_name')
    url = request.POST.get('lecture_url')
    desc = request.POST.get('trans_script')
    start = request.POST.get('start')
    end = request.POST.get('end')
    his_classroom = classrooms.objects.get(user=request.user)
    new_lecture = lectures(classroom = his_classroom,lecture_name=name,lecture_url=url,start_time=start,end_time=end,trans_script=desc)
    new_lecture.save()
    return HttpResponse('success')

def autocompleteclassroom(request):
	text = request.GET.get('term', '')
	results = classrooms.objects.filter(course_name__contains = text,user=request.user)
	res = []
	for classroom in results:
		drug_json = {}
		drug_json['id'] = classroom.id
		drug_json['label'] = classroom.course_name
		drug_json['value'] = classroom.course_name
		res.append(drug_json)
	data = json.dumps(res)

	mimetype = 'application/json'
	return HttpResponse(data, mimetype)

def show_lectures(request,classes_id):
    class_lectures = lectures.objects.filter(classroom=classrooms.objects.get(id=classes_id))
    return render(request,'lectures.html',{'lectures':class_lectures})

def upvote(request):
    classes_id = request.POST.get('class_id')
    c_room = classrooms.objects.get(id=classes_id)
    already_vote = vote_classroom.objects.filter(user=request.user,classroom=c_room).first()
    if already_vote is None:
        newvote = vote_classroom(classroom=c_room,user=request.user,vote_type=True)
        newvote.save()
        c_room.upvote_cnt +=1
        c_room.save()
        return HttpResponse('upvoted')
    else:
        if already_vote.vote_type == False:
            already_vote.vote_type = True
            c_room.upvote_cnt +=1
            c_room.downvote_cnt-=1
            c_room.save()
            already_vote.save()
        return HttpResponse('already upvoted')

def downvote(request):
    classes_id = request.POST.get('class_id')
    c_room = classrooms.objects.get(id=classes_id)
    already_vote = vote_classroom.objects.filter(user=request.user,classroom=c_room).first()
    if already_vote is None:
        newvote = vote_classroom(classroom=c_room,user=request.user,vote_type=False)
        newvote.save()
        c_room.downvote_cnt +=1
        c_room.save()
        return HttpResponse('downvoted')
    else:
        if already_vote.vote_type == True:
            already_vote.vote_type = False
            c_room.downvote_cnt +=1
            c_room.upvote_cnt-=1
            c_room.save()
            already_vote.save()
        return HttpResponse('already downvoted')
