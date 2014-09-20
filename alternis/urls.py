from django.conf.urls import patterns, include, url
from django.contrib import admin
from alternisApp import views


urlpatterns = patterns('',
    (r'^alternisApp/$', 'alternisApp.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    (r'^alternisApp/(?P<Search>.*)', 'alternisApp.views.query')
)
