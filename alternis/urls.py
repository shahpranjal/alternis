from django.conf.urls import patterns, include, url
from django.contrib import admin
from alternisApp import views


urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^query/', views.query)
)
