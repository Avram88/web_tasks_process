from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'web_tasks_process.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^tasks/', include('tasks.urls', namespace='tasks')),
    url(r'^admin/', include(admin.site.urls)),    
)
