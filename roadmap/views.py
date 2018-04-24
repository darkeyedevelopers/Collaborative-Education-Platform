# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Roadmap,Step,Resource,Upvote,Downvote
from django.utils import timezone
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth import authenticate,login


# Create your views here.
def roadmap_list(request):
    roadmaps = Roadmap.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    print len(roadmaps)
    return render(request, 'roadmap/roadmap_list.html', {'roadmaps': roadmaps})


def roadmap_detail(request, pk):
    roadmap = get_object_or_404(Roadmap, pk=pk)
    steps=Step.objects.filter(roadmap=roadmap)
    resources = Resource.objects.filter(roadmap=roadmap)
    return render(request, 'roadmap/roadmap_detail.html', {'roadmap': roadmap,'steps':steps,'resources':resources})


def prevcancel(user,roadmap):
    upvotes=Upvote.objects.filter(roadmap=roadmap,user=user)
    if(len(upvotes)>0):
        roadmap.upcount-=1
        roadmap.save()
        upvotes.delete()
    downvotes = Downvote.objects.filter(roadmap=roadmap, user=user)
    if (len(downvotes) > 0):
        roadmap.downcount -= 1
        roadmap.save()
        downvotes.delete()


def upvote(request,pk):
    print "In Upvote"
    roadmap = get_object_or_404(Roadmap, pk=pk)
    prevcancel(request.user,roadmap)
    upvote=Upvote()
    upvote.user=request.user
    upvote.roadmap=roadmap
    upvote.save()
    roadmap.upcount += 1
    roadmap.save()
    return redirect('roadmap:roadmap_detail',pk=pk)

def downvote(request,pk):
    print "In Downvote"
    roadmap = get_object_or_404(Roadmap, pk=pk)
    prevcancel(request.user, roadmap)
    downvote = Downvote()
    downvote.user = request.user
    downvote.roadmap = roadmap
    downvote.save()
    roadmap.downcount += 1
    roadmap.save()
    return redirect('roadmap:roadmap_detail',pk=pk)
\
'''
def road_new(request):
    if request.method == "POST":
        form = RoadmapForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.session['user']
            post.published_date = timezone.now()
            post.save()
            return render(request, 'blog/post_detail.html', {'post': post})

    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def road_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return render(request, 'blog/post_detail.html', {'post': post})
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
'''

def logout(request):
    del request.session['user']
    print("logout")
    return redirect('login:index')
