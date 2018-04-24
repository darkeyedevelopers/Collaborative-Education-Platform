from django.contrib import admin
from django.contrib import messages
from django.apps import apps
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.management import call_command
from importlib import import_module
from django.conf import settings
from django.core.urlresolvers import clear_url_caches
from django.shortcuts import render, redirect
from Accounts.forms import SignUpForm
from .models import Profile
from django.db import models
import urllib
from datetime import datetime
import urllib2
from django.utils.translation import ugettext as _


from django.contrib.auth.models import User
import json

def signup(request):
	if request.method == 'POST':
		form = SignUpForm (request.POST )
		if form.is_valid ():
			user = form.save ()
			user.refresh_from_db ()  # load the profile instance created by the signal
			user.profile.full_name = form.cleaned_data.get ('full_name')
			user.profile.mob_number = form.cleaned_data.get ('mob_number')
			user.profile.email_id = form.cleaned_data.get ('email_id')
			user.email = user.profile.email_id
			user.save ()
			raw_password = form.cleaned_data.get ('password1')
			user = authenticate (username=user.username, password=raw_password)
			login (request, user)
			return redirect ('/dashboard/')
		else:
			return render (request, 'Accounts/signup.html', {'form': form})
	else:
		form = SignUpForm ()
	return render (request, 'Accounts/signup.html', {'form': form})
