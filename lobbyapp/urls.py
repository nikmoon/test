from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^login/$', views.login_view),
    url(r'^logout/$', views.logout_view),
    url(r'^registration/$', views.registration_view),
    url(r'^get_new_messages/$', views.get_new_messages),
    url(r'^create_lobby/$', views.create_lobby),
    url(r'^join_lobby/$', views.join_lobby),
    url(r'^$', views.index),
]