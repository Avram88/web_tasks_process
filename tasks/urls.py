from django.conf.urls import patterns, url

from tasks import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.auth_login, name='login'),
    url(r'^logout/$', views.auth_logout, name='logout'),
    url(r'^sign_in/$', views.sign_in, name='sign_in'),
    url(r'^(?P<model_name>\w+)/start_process/$', views.start_process, name='start_process'),
    url(r'^(?P<task_id>\d+)/detail/$', views.detail, name='detail'),
    url(r'^(?P<task_id>\d+)/finish_task/$', views.finish_task, name='finish_task'),
)