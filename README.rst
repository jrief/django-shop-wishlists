=======================
django SHOP - Wishlists
=======================

This app's purpose is to provide wishlists to django-shop, so that customers
can remember items together with their variation for later acquisition.

A wishlist is quite similar to the shopping cart. The differences are, that a
wishlist does not keep information about product quantities nor does a wishlist
manage any extra item fields, such as taxes.
But unlike the cart, each customer may have one to many wishlists. Wishlists
currently are not visible to other customers, but that might change in the
future.

For obvious reasons, wishlists can not be assigned to an anonymous user. A
wishlist must be bound to an authenticated user. Therefore, the shop must offer
some authentication methods, so that each customer can login and/or
register himself. Attempting to add a product to a wishlist without being
authenticated, raises a PermissionDenied exception. This exception may be
catched, so that the user then is redirect onto a login page.

Each customer always has one and only one active wishlist. He can add and delete 
products only from this wishlist. A wishlist is created the first time, a
customer adds a product to a wishlist. If the customer is an anonymous user at
that time, either redirect him to a  login page in your shop, or disable the
``Add to wishlist`` buttons. 

Installation
------------
This requires a patched version of django SHOP 
https://github.com/jrief/django-shop/tree/variations
which offers a simpler interface to products variations.

Usage
-----

Add ``shop_wishlists`` to your ``INSTALLED_APPS`` in your settings.py

Run::

   python manage.py schemamigration --initial shop_wishlists
   python manage.py migrate shop_wishlists

to add the tables ``shop_wishlist`` and ``shop_wishlist_item`` to the database
models.

Change your code
================

To your urls.py, add the following line::

    (r'^shop/wishlist/', include('shop_wishlists.urls')),

Copy the template ``wishlist.html`` to your shop and adopt it according to your
needs.

Add to your products detail view the following mixin class::

   from shop.views.product import ProductDetailView
   from shop_wishlists.views import WishlistProductDetailViewMixin
   
   class MyProductDetailView(WishlistProductDetailViewMixin, ProductDetailView):
       ...

To the form of your products detail view, add the following template code::

    <button type="submit" name="product_action" value="add_to_wishlist">
        {% trans "Add to wishlist" %}
    </button>

this will add a button to your products detail view, so that a customer can 
add the product to the wishlist. If variations have been defined for this
product, these are also stored in the wishlist.

The context of your products detail view contains an additional boolean variable,
``product_on_active_wishlist`` which is true if the product is already on the
active wishlist. This is a convenience to inform the customer, if he already
added the product to the wishlist.

If MyProductDetailView define a post() method, it shall delegate the post
request to the mixin class using::

    def post(self, *args, **kwargs):
        ...
        super(MyProductDetailView, self).post(*args, **kwargs)
        ...

this post method then itself delegates the post request to the other mixin
classes declared in `MyProductDetailView`.


Multiple wishlists
------------------

More than 90% of all customers never need more than one wishlist. If your
customers fall into this category, do not embarrass them with the possibility to
create more than one wishlist. Offering more than one wishlist means that you
also have to add functionality to switch between wishlists, remove and rename
them.

But in case you want to offer more than one wishlist, the API of
django-shop-wishlists offers all the required functionality.


Utility functions
=================

By calling::

   utils.get_or_create_wishlist

the default wishlist for the current authenticated customer is created or 
retrieved from the database. This wishlist then becomes the active wishlist, and
all of the following operations are applied onto that wishlist:

* You may add and remove an item from the wishlist.
* Copy an item from the wishlist to the cart.
* Create an additional wishlist
* Switch between the wishlists for the current customer
* Rename the active wishlist
* Delete the active wishlist - this activates the next wishlist from the pool.
  If you deleted the last wishlist a new wishlist is created.

Note that items on the wishlist keep the information about their product
variations, independently from the chosen variation model.

Contributing
============

Feel free to fork this project on github, send pull requests...
development discussion happens on the django SHOP mailing list
https://groups.google.com/forum/#!forum/django-shop
