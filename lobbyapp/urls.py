from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^login/$', views.login_view),
    url(r'^logout/$', views.logout_view),
    url(r'^registration/$', views.registration_view),
    url(r'^get_new_messages/$', views.get_new_messages),
    url(r'^create_lobby/$', views.create_lobby),
    url(r'^lobby/$', views.lobby_view),
    url(r'^join_lobby/([0-9]{1,10})/$', views.join_lobby),
    url(r'^game/$', views.start_game),
    url(r'^$', views.index),
]