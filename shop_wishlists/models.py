# -*- coding: utf-8 -*-
from hashlib import sha1
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import simplejson as json
from jsonfield.fields import JSONField
from shop.models.productmodel import Product
from shop.models.defaults.bases import BaseCartItem


class Wishlist(models.Model):
    """
    Each customer, ie. user may have one or more wishlists to remember items 
    for later acquisition.
    """
    user = models.ForeignKey(User)
    name = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        db_table = 'shop_wishlist'
        verbose_name = _('Wishlist')
        verbose_name_plural = _('Wishlists')

    def add_product(self, product, variation=None):
        """
        Adds the exact product to this wishlist, if it is not already there.
        """
        variation_hash = self._get_variation_hash(variation)
        items = WishlistItem.objects.filter(wishlist=self, product=product, 
                                            variation_hash=variation_hash)
        if not items.exists():
            item = WishlistItem.objects.create(wishlist=self, product=product,
                           variation=variation, variation_hash=variation_hash)
            item.save()
        self.save() # to get the last updated timestamp for this wishlist

    def get_all_items(self):
        """
        Return all items of this wishlist
        """
        return WishlistItem.objects.filter(wishlist=self)
        
    def find_item(self, product, variation=None):
        """
        For a given product and its variation, find an entry in this wishlist 
        and return the found WishlistItem or None.
        """
        variation_hash = self._get_variation_hash(variation)
        return WishlistItem.objects.filter(wishlist=self, product=product, 
                                            variation_hash=variation_hash)

    def delete_item(self, item):
        """
        A simple convenience method to delete an item from the wishlist.
        """
        WishlistItem.objects.get(pk=item.id).delete()
        self.save()

    def _get_variation_hash(self, variation):
        if variation:
            serialized_variation = json.dumps(variation, cls=DjangoJSONEncoder,
                                              sort_keys=True)
            variation_hash = sha1(serialized_variation).hexdigest()
        else:
            variation_hash = None
        return variation_hash


class WishlistItem(models.Model):
    """
    This is a holder for the item in the wishlist.
    """
    wishlist = models.ForeignKey(Wishlist)
    product = models.ForeignKey(Product)
    variation = JSONField(null=True, blank=True)
    variation_hash = models.CharField(max_length=64, null=True)

    class Meta(object):
        db_table = 'shop_wishlist_item'
        verbose_name = _('Wishlist item')
        verbose_name_plural = _('Wishlist items')
