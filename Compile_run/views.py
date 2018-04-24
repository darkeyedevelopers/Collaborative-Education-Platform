from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from dashboard.models import snippets
import subprocess
from django.template import loader
import datetime
from threading import Thread
import time
import json
import select
from django.utils.html import escape
import signal,os
from signal import SIG_DFL

idealbuffer = 1

def index(request):
	return render(request,'submission/Drop.html',{'Lang':'c'})

def get_u(request):
	try:
		u = request.session['user']
	except:
		return ''
	return u

def safe_escape(ans):
	try:
		ans = escape(ans)
	except Exception:
		ans = '-{ truncated }--Provide neat input'
	return ans


def deletefromtree(request,command,user):
	all_info,err = subprocess.Popen('ps --forest -o pid,cmd -g $(ps -o sid= -p '+str(command.pid)+')',shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).communicate()
	rows = all_info.split("\n")
	print user.username
	time_out = False
	for i in rows:
		row = i.strip(' ')
		at = row.find('All/'+request.user.username)
		if at > 0 :
			pid = row.split(" ")[0]
			subprocess.Popen('kill '+pid,shell=True).communicate()
			print pid , 'killed from server'
			time_out=True
	return time_out

def getWelO(ans):
	s1 = ans.split("\n")
	s2 = []

	for string in s1 :
		string = string.strip(" ")
		string = string.strip("\r")
		if string is "\n" or string == '':
			continue
		s2.append(string)
	ans = '\n'.join(s2)
	return ans

def getO(request,command,timeout,user):
	poll_obj = select.poll()
	poll_obj.register(command.stdout, select.POLLIN)
	buflimit = 409800
	buf = 0
	ans =''
	start = time.time()

	while buf <= buflimit and start + timeout > time.time() :
		poll_result = poll_obj.poll(0)
		if poll_result:
			ans+= command.stdout.read(idealbuffer)
			buf+=idealbuffer

	return getWelO(ans),deletefromtree(request,command,user)

def change(request):
	if request.method == 'POST':
		Lang = request.POST.get('lang')
		c_snippet = snippets.objects.filter(user=request.user).first()
		if c_snippet is not None:
			if Lang == 'c':
				return HttpResponse(c_snippet.c_code)
			elif Lang == 'c_cpp':
				return HttpResponse(c_snippet.cpp_code)
			elif Lang == 'java':
				return HttpResponse(c_snippet.java_code)
			elif Lang == 'python':
				return HttpResponse(c_snippet.py_code)
			elif Lang == 'python3':
				return HttpResponse(c_snippet.py3_code)
		return HttpResponse('default code')


def run(request):
	if request.method == 'POST':
		time_out=False
		code = request.POST.get('code')
		Lang = request.POST.get('lang')
		status = request.POST.get('Check_Status')
		errors = ''
		input_from_user = request.POST.get('input')
		if input_from_user is None:
			input_from_user=''

		snippet = snippets.objects.filter(user=request.user).first()


		if snippet is None:
			snippet = snippets(user=request.user,lang=Lang,code='',result='',desc='')

		if Lang == 'c':
			snippet.c_code = code
			snippet.save()
			file_name = 'All/'+request.user.username+'cSolution.c'
			file = open (file_name, 'w')
			file.write (code)
			#print ('File created')
			file.close ()
			ans = ''
			command = subprocess.Popen ('gcc All/'+request.user.username+'cSolution.c -lm -o All/'+request.user.username, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

			ans,err = command.communicate()
			subprocess.Popen('kill '+str(command.pid),shell=True)

			if (len (ans) > 1):
				return  HttpResponse("<pre class=\"ui segment\" style=\"background-color: #f8f8f8;border:0px;\">" + safe_escape(ans) + "</pre>")
			else:
				ans = ''
				#print ('test')

				command = subprocess.Popen ("./All/"+request.user.username, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
				#print ("testing .out created")
				command.stdin.write (input_from_user)
				command.stdin.close ()
				timeout = 3
				ans,time_out = getO(request,command,timeout,request.user)
			if time_out:
				return HttpResponse("<pre class=\"ui segment\" style=\"background-color: #f8f8f8;border:0px;\">"+"Terminate due to timeout"+"\n\n\nYour Output : \n"+safe_escape(ans)+"</pre>")
			return HttpResponse("<pre class=\"ui segment\" style=\"background-color: #f8f8f8;border:0px;\">" + safe_escape(ans) + "</pre>")


		elif Lang == 'c_cpp':
			snippet.cpp_code = code
			snippet.save()
			file_name = 'All/'+request.user.username+'Solution.cpp'
			file = open (file_name, 'w')
			file.write (code)
			#print ('File created')
			file.close ()
			ans = ''
			command = subprocess.Popen ('g++ All/'+request.user.username+'Solution.cpp -lm -o All/'+request.user.username, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

			ans,err = command.communicate()
			subprocess.Popen('kill '+str(command.pid),shell=True)

			if (len (ans) > 1):
				return  HttpResponse("<pre class=\"ui segment\" style=\"background-color: #f8f8f8;border:0px;\">" + safe_escape(ans) + "</pre>")
			else:
				ans = ''
				#print ('test')

				command = subprocess.Popen ("./All/"+request.user.username, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
				#print ("testing .out created")
				command.stdin.write (input_from_user)
				command.stdin.close ()
				timeout = 3
				ans,time_out = getO(request,command,timeout,request.user)
			if time_out:
				return HttpResponse("<pre class=\"ui segment\" style=\"background-color: #f8f8f8;border:0px;\">"+"Terminate due to timeout"+"\n\n\nYour Output : \n"+safe_escape(ans)+"</pre>")
			return HttpResponse("<pre class=\"ui segment\" style=\"background-color: #f8f8f8;border:0px;\">" + safe_escape(ans) + "</pre>")

		elif Lang == 'java':
				snippet.java_code = code
				snippet.save()
				file_name = 'All/Solution.java'
				file = open (file_name, 'w')
				file.write (code)
				#print ('File created')
				file.close ()
				ans = ''
				command = subprocess.Popen ('javac All/'+'Solution.java ', shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

				ans,err = command.communicate()
				subprocess.Popen('kill '+str(command.pid),shell=True)

				if (len (ans) > 1):
					return  HttpResponse("<pre class=\"ui segment\" style=\"background-color: #f8f8f8;border:0px;\">" + safe_escape(ans) + "</pre>")
				else:
					ans = ''
					#print ('test')

					command = subprocess.Popen ("java -cp All/ Solution", shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
					#print ("testing .out created")
					command.stdin.write (input_from_user)
					command.stdin.close ()
					timeout = 3
					ans,time_out = getO(request,command,timeout,request.user)
				if time_out:
					return HttpResponse("<pre class=\"ui segment\" style=\"background-color: #f8f8f8;border:0px;\">"+"Terminate due to timeout"+"\n\n\nYour Output : \n"+safe_escape(ans)+"</pre>")
				return HttpResponse("<pre class=\"ui segment\" style=\"background-color: #f8f8f8;border:0px;\">" + safe_escape(ans) + "</pre>")

		elif Lang == 'python':

			snippet.py_code = code
			snippet.save()
			file_name = 'All/'+request.user.username+'Solution.py'
			file = open (file_name, 'w')
			file.write (code)
			file.close ()
			ans = ''
			command = subprocess.Popen ('python All/'+request.user.username+'Solution.py', shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
			command.stdin.write (input_from_user)
			command.stdin.close ()
			timeout = 3
			ans,time_out = getO(request,command,timeout,request.user)
			if time_out:
				return HttpResponse("<pre class=\"ui segment\" style=\"background-color: #f8f8f8;border:0px;\">"+"Terminate due to timeout"+"\n\n\nYour Output : \n"+safe_escape(ans)+"</pre>")
			return HttpResponse("<pre class=\"ui segment\" style=\"background-color: #f8f8f8;border:0px;\">" + safe_escape(ans) + "</pre>")

		elif Lang == 'python3':

			snippet.py3_code = code
			snippet.save()
			file_name = 'All/'+request.user.username+'Solution.py'
			file = open (file_name, 'w')
			file.write (code)
			file.close ()
			ans = ''
			command = subprocess.Popen ('python3 All/'+request.user.username+'Solution.py', shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
			command.stdin.write (input_from_user)
			command.stdin.close ()
			timeout = 3
			ans,time_out = getO(request,command,timeout,request.user)
			if time_out:
				return HttpResponse("<pre class=\"ui segment\" style=\"background-color: #f8f8f8;border:0px;\">"+"Terminate due to timeout"+"\n\n\nYour Output : \n"+safe_escape(ans)+"</pre>")
			return HttpResponse("<pre class=\"ui segment\" style=\"background-color: #f8f8f8;border:0px;\">" + safe_escape(ans) + "</pre>")

		elif Lang == 'html':
			snippet=snippets.objects.filter(user=request.user)
			code = request.POST.get('code')
			if snippet is None :
				snippet = snippets(user=request.user)
				snippet.html = code
				snippet.save()
			else:
				snippet.html = code
				snippet.save()
			return render(request,'Web_Drop.html',{'session':code})
