# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from views import WishlistDetailView


urlpatterns = patterns('',
    url(r'^$', WishlistDetailView.as_view(), name='wishlist'),
    url(r'^update/$', WishlistDetailView.as_view(action='put'), name='wishlist_update'),
    )
