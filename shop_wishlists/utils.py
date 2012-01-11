# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.core import exceptions
from shop_wishlists.models import Wishlist, WishlistItem


def get_or_create_wishlist(request):
    """
    Each user may have one or more wishlists. Find the active one or create one
    with a default name.
    """
    if request.user is None or not request.user.is_authenticated():
        raise exceptions.PermissionDenied('A wishlist can not be assigned to an anonymous user')
    if not hasattr(request, '_wishlist'):
        active_wishlist = request.session.get('active_wishlist')
        if active_wishlist:
            wishlist = Wishlist.objects.get(pk=active_wishlist)
        else:
            wishlist = Wishlist.objects.filter(user=request.user)
            if wishlist:
                wishlist = wishlist[0]
            else:
                wishlist = Wishlist.objects.create(user=request.user, name=_('My wishlist'))
            request.session['active_wishlist'] = wishlist.id
        setattr(request, '_wishlist', wishlist)
    return getattr(request, '_wishlist')


def is_product_on_active_wishlist(request, product):
    """
    Returns true if the given product is on the active wishlist.
    Product variations are intentionally not considered, so that this function
    can be used to display the consumer, that this product is on the wishlist
    without having him to re-choose their variations.
    """
    wishlist = get_or_create_wishlist(request)
    items = WishlistItem.objects.filter(wishlist=wishlist, product=product)
    return items.exists()


def create_additional_wishlist(request, name=None):
    """
    Create an additional wishlist and set is as active wishlist.
    If no name is given (the default), a useful name is assigned to the new wishlist. 
    """
    if request.user is None or not request.user.is_authenticated():
        raise exceptions.PermissionDenied('A wishlist can only be created by an authenticated user')
    if name is None:
        name = _('My wishlist %s') % (Wishlist.objects.filter(user=request.user).count()+1)
    wishlist = Wishlist.objects.create(user=request.user, name=name)
    request.session['active_wishlist'] = wishlist.id
    setattr(request, '_wishlist', wishlist)
    return wishlist


def switch_wishlist(request, wishlist_id):
    """
    Set the wishlist with the given id as the active wishlist.
    """
    wishlist = Wishlist.objects.get(user=request.user, pk=wishlist_id)
    request.session['active_wishlist'] = wishlist.id
    setattr(request, '_wishlist', wishlist)
    return wishlist


def rename_active_wishlist(request, name):
    """
    Rename the active wishlist.
    """
    if hasattr(request, '_wishlist'):
        wishlist = getattr(request, '_wishlist')
    else:
        active_wishlist = request.session.get('active_wishlist')
        if not active_wishlist:
            raise exceptions.ObjectDoesNotExist('No active wishlist for this session')
        wishlist = Wishlist.objects.get(pk=active_wishlist)
        setattr(request, '_wishlist', wishlist)
    wishlist.name = name
    wishlist.save()


def delete_active_wishlist(request):
    """
    Deletes the active wishlist together with all stored items.
    """
    if hasattr(request, '_wishlist'):
        wishlist = getattr(request, '_wishlist')
        delattr(request, '_wishlist')
    else:
        active_wishlist = request.session.get('active_wishlist')
        if not active_wishlist:
            raise exceptions.ObjectDoesNotExist('No active wishlist for this session')
        wishlist = Wishlist.objects.get(pk=active_wishlist)
    Wishlist.objects.get(pk=wishlist.id).delete()
    del request.session['active_wishlist']

