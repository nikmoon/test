from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index),
#    url(r'^registration/$', views.registration),
    url(r'^registration/$', views.RegisterFormView.as_view()),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
]