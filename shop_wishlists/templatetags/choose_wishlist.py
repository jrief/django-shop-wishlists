from django import template
from shop_wishlists.models import Wishlist


register = template.Library()


@register.inclusion_tag('templatetags/_choose_wishlist.html', takes_context=True)
def choose_wishlist(context):
    request = context['request']
    wishlists = Wishlist.objects.filter(user=request.user)
    active_wishlist = request.session.get('active_wishlist')
    print active_wishlist
    return {
        'wishlists': wishlists,
        'active_wishlist': active_wishlist,
    }
