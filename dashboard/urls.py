from django.conf.urls import url
from . import views
from django.conf.urls import url,include

app_name = 'dashboard'

urlpatterns = [
    url(r'^$', views.index,name='index'),
    url(r'^tocreateroom',views.tocreateroom,name='tocreateroom'),
    url(r'^createroom',views.createroom,name='createroom'),
    url(r'^toaddlecture',views.toaddlecture,name='toaddlecture'),
    url(r'^addlecture',views.addlecture,name='addlecture'),
    url(r'^autocompleteclassroom/$',views.autocompleteclassroom,name='autocompleteclassroom'),
    url(r'^show_lectures/(?P<classes_id>[0-9]+)/$',views.show_lectures,name='show_lectures'),
    url(r'^upvote/$',views.upvote,name='upvote'),
    url(r'^downvote/$',views.downvote,name='downvote'),
]
