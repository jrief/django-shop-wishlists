#-*- coding: utf-8 -*-
from django import forms
from django.forms.models import modelformset_factory
from shop_wishlists.models import WishlistItem


class WishlistItemModelForm(forms.ModelForm):
    """A form for the WishlistItem model. To be used in the WishlistDetailView."""

    class Meta:
        model = WishlistItem

#    def save(self, *args, **kwargs):
#        """
#        We don't save the model using the regular way here because the
#        Cart's ``update_quantity()`` method already takes care of deleting
#        items from the cart when the quantity is set to 0.
#        """
#        print "save form"
#        quantity = self.cleaned_data['quantity']
#        instance = self.instance.cart.update_quantity(self.instance.id,
#                quantity)
#        return instance


def get_wishlist_formset(wishlist_items=None, data=None):
    """
    Returns a WislistItemFormSet which can be used in the WislistDetailView.

    :param wishlist_items: The queryset to be used for this formset. This should
      be the list of updated cart items of the current cart.
    :param data: Optional POST data to be bound to this formset.
    """
    assert(wishlist_items is not None)
    WislistItemFormSet = modelformset_factory(WishlistItem,
                                            form=WishlistItemModelForm, extra=0)
    kwargs = { 'queryset': wishlist_items, }
    form_set = WislistItemFormSet(data, **kwargs)

    # The Django ModelFormSet pulls the item out of the database again and we
    # would lose the updated line_subtotals
    for form in form_set:
        for item in wishlist_items:
            if form.instance.id == item.id:
                form.instance = item
    return form_set
