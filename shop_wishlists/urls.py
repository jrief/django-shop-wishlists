# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from views import WishlistDetailView


urlpatterns = patterns('',
    url(r'^$', WishlistDetailView.as_view(), name='wishlist'),
    url(r'^rename/$', WishlistDetailView.as_view(handler='rename'),
        name='wishlist_rename'),
    url(r'^delete/$', WishlistDetailView.as_view(handler='delete'),
        name='wishlist_delete'),
)
