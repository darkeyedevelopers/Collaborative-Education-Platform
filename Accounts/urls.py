from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'Accounts'

urlpatterns = [
	url(r'^login/$',auth_views.login,{'template_name': 'login.html'},name='login'),
	url(r'^logout/$',auth_views.logout, name='logout', kwargs={'next_page': '/Accounts/login'}),
	url(r'^signup/$', views.signup, name='signup'),
]
