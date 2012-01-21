=======================
django SHOP - Wishlists
=======================

This app's purpose is to provide wishlists to django-shop, so that customers
can remember items together with their variation for later acquisition.

Installation
============

This module requires a version of django SHOP which offers functionality for
a simpler integration of products variations, see 
https://github.com/jrief/django-shop/tree/variations.

Add `shop_wishlists` to your INSTALLED_APPS in your settings.py

Run::

   python manage.py schemamigration --initial shop_wishlists
   python manage.py migrate shop_wishlists

to add the database models.
For obvious reasons, wishlists can not be assigned to an anonymous user. A
wishlist must be bound to an authenticated user. Therefore, the shop must offer
some authentication methods, so that each customer can login and/or
register himself.

Usage
=====

A wishlist is quite similar to the shopping cart. The differences are, that a
wishlist does not keep information about product quantities nor does a wishlist
manage any extra item fields, such as taxes.
But unlike the cart, each customer may have one to many wishlists.

Each customer always has one and only one active wishlist. He can add and delete 
products only from this wishlist.

A wishlist is created the first time, a customer adds a product to a wishlist.
If the customer is an anonymous user at that time, either redirect him to a 
login page in your shop, or disable the "Add to wishlist" buttons. The attempt
to add a product to a wishlist without being authenticated, raises a
PermissionDenied exception. This exception may be catched, so that the user then
is redirect onto a login page.

By calling::

   utils.get_or_create_wishlist

the default wishlist for the current authenticated customer is created or 
retrieved from the database. This wishlist then becomes the active wishlist, and
all of the following operations are applied onto that wishlist:

* You may add and remove an item from the wishlist.
* Copy an item from the wishlist to the cart.
* Create an additional wishlist, switch between these wishlists, rename the
active wishlist and delete it.

Note that items on the wishlist keep the information about their product
variations, independently from the chosen variation model.

Multiple wishlists
------------------

More than 90% of all customer will never need more than one wishlist. If your
customers fall into this category, do not embarrass them with the possibility to
create more than one wishlist. Offering more than one wishlist means that you
also have to add functionality to switch between wishlists, remove and rename
them.
But in case you want to offer more than one wishlist, all the required
functionality is available in django-shop-wishlists.

Contributing
============

Feel free to fork this project on github, send pull requests...
development discussion happens on the django SHOP mailing list
https://groups.google.com/forum/#!forum/django-shop
