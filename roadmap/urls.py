from django.conf.urls import url
from . import views

app_name = 'roadmap'


urlpatterns = [
    url(r'^$', views.roadmap_list, name='roadmap_list'),
    url(r'^(?P<pk>\d+)/$', views.roadmap_detail, name='roadmap_detail'),
    url(r'^upvote/(?P<pk>\d+)/$', views.upvote, name='upvote'),
    url(r'^downvote/(?P<pk>\d+)/$', views.downvote, name='downvote'),
    url(r'^logout/$', views.logout, name='logout'),
]