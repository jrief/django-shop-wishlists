# -*- coding: utf-8 -*-
from models import Wishlist
from utils import get_or_create_wishlist, is_product_on_active_wishlist


class WishlistDetailViewMixin(object):
    """
    An abstraction class to mix in functionality for wishlists
    """
    def get_context_data(self, **kwargs):
        context = super(WishlistDetailViewMixin, self).get_context_data(**kwargs)
        product = self.get_object()
        context.update({ 'product_on_active_wishlist': is_product_on_active_wishlist(self.request, product) })
        return context

    def post(self, *args, **kwargs):
        super(WishlistDetailViewMixin, self).post(*args, **kwargs)
        if self.request.POST['product_action'] == 'add_to_wishlist':
            self.add_to_wishlist()

    def add_to_wishlist(self):
        wishlist = get_or_create_wishlist(self.request)
        product = self.get_object()
        if hasattr(self, 'get_variation') and callable(self.get_variation):
            variation = self.get_variation(product)
        else:
            variation = None
        wishlist.add_product(product, variation)
        wishlist.save()
