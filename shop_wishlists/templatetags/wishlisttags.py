from django import template
from shop_wishlists.models import Wishlist


register = template.Library()

@register.inclusion_tag('templatetags/_select_wishlist.html', takes_context=True)
def select_wishlist(context):
    request = context['request']
    context.update({ 
        'wishlists': Wishlist.objects.filter(user=request.user),
        'active_wishlist': request.session.get('active_wishlist'),
    })
    return context
