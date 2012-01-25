# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.core import exceptions
from django.http import HttpResponse, HttpResponseRedirect
from shop.views import ShopView, ShopTemplateResponseMixin
from models import Wishlist
from forms import get_wishlist_formset
from utils import get_or_create_wishlist, is_product_on_active_wishlist, \
    copy_item_to_cart, create_additional_wishlist, switch_wishlist, \
    rename_active_wishlist, delete_active_wishlist


class WishlistProductDetailViewMixin(object):
    """
    An abstraction class to mix in ProductDetailView for wishlists
    """
    def get_context_data(self, **kwargs):
        context = super(WishlistProductDetailViewMixin, self).get_context_data(**kwargs)
        product = self.get_object()
        context.update({ 'product_on_active_wishlist': 
                        is_product_on_active_wishlist(self.request, product) })
        return context

    def post(self, *args, **kwargs):
        super(WishlistProductDetailViewMixin, self).post(*args, **kwargs)
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
    handler = None

    def dispatch(self, request, *args, **kwargs):
        """
        If `handler` is defined use it dispatch request to the right method.
        """
        if not self.handler:
            return super(WishlistDetailView, self).dispatch(request, *args,
                **kwargs)
        handler = getattr(self, self.handler)
        self.request = request
        self.args = args
        self.kwargs = kwargs
        return handler()

    def get(self, request, *args, **kwargs):
        if request.GET.has_key('select_wishlist'):
            if request.GET['select_wishlist']=='add_wishlist':
                wishlist = create_additional_wishlist(request)
            else:
                wishlist_id = int(request.GET['select_wishlist'])
                wishlist = switch_wishlist(request, wishlist_id)
        else:
            wishlist = get_or_create_wishlist(self.request)
        context = {}
        context.update({ 'wishlist_name': wishlist.name })
        context.update({ 'wishlist_date_created': wishlist.date_created })
        context.update({ 'wishlist_last_updated': wishlist.last_updated })
        formset = get_wishlist_formset(wishlist_items=wishlist.get_all_items())
        context.update({ 'formset': formset })
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        if request.POST.has_key('add_to_cart'):
            copy_item_to_cart(self.request, int(self.request.POST['add_to_cart']))
        elif request.POST.has_key('remove_item'):
            wishlist = get_or_create_wishlist(self.request)
            wishlist.delete_item(int(self.request.POST['remove_item']))
        else:
            raise exceptions.FieldError('Missing field in form')
        return self.success()

    def rename(self):
        """
        Remove active wishlist
        """
        rename_active_wishlist(self.request, self.request.POST['wishlist_name'])
        return self.success()

    def delete(self):
        """
        Delete active wishlist
        """
        delete_active_wishlist(self.request)
        return self.success()

    def success(self):
        if self.request.is_ajax():
            return HttpResponse('Ok<br />')
        else:
            return HttpResponseRedirect(reverse('wishlist'))
