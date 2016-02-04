# -*- coding: utf-8 -*-
__author__ = 'vladimir.pekarsky'

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.listing),
    url(r'^change_experience/([0-9]+)/',
        views.change_player_experience),
    url(r'^login/$', views.login_custom),
    url(r'^logout/$', views.logout_custom),
]