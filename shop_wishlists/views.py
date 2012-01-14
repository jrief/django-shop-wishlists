# -*- coding: utf-8 -*-
from shop.views import ShopView, ShopTemplateResponseMixin
from models import Wishlist
from forms import get_wishlist_formset
from utils import get_or_create_wishlist, is_product_on_active_wishlist


class ProductDetailViewMixin(object):
    """
    An abstraction class to mix in ProductDetailView for wishlists
    """
    def get_context_data(self, **kwargs):
        context = super(ProductDetailViewMixin, self).get_context_data(**kwargs)
        product = self.get_object()
        context.update({ 'product_on_active_wishlist': 
                        is_product_on_active_wishlist(self.request, product) })
        return context

    def post(self, *args, **kwargs):
        super(ProductDetailViewMixin, self).post(*args, **kwargs)
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


class WishlistDetailView(ShopTemplateResponseMixin, ShopView):
    model = Wishlist
    template_name = 'wishlist.html'
    action = None

    def get(self, request, *args, **kwargs):
        wishlist = get_or_create_wishlist(self.request)
        context = {}
        context.update({ 'wishlist_name': wishlist.name })
        context.update({ 'wishlist_date_created': wishlist.date_created })
        context.update({ 'wishlist_last_updated': wishlist.last_updated })
        formset = get_wishlist_formset(wishlist_items=wishlist.get_all_items())
        context.update({'formset': formset, })
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        print "post TODO"

    def delete(self, request, *args, **kwargs):
        print "post TODO"