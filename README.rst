=======================
django SHOP - Wishlists
=======================

This app's purpose is to provide wishlists to django-shop, so that customers
can remember items together with their variation for later acquisition.

This code is work in progress.


Installation
============

This module requires a version of django SHOP which offers functionality for
a simpler interface to products variations, see 
https://github.com/jrief/django-shop/tree/variations.

* Add `shop_wishlists` to your INSTALLED_APPS in your settings.py
* Run::
   python manage.py schemamigration --initial shop_wishlists
   python manage.py migrate shop_wishlists
to add the database models.
Wishlists must be bound to an authenticated user. For obvious reasons, they can
not be assigned to an anonymous user, ie. a session only. Therefore, the shop
must offer some authentication methods, so that each customer can login and/or
register himself.

Usage
=====

A wishlist is created the first time, a customer adds a product to a wishlist.
If the customer is an anonymous user at that time, redirect him to a page in
your shop, so that he can authenticate himself.
Since more than 95% of all customer never need more than one wishlist, don't
embarrass them with creating a specially named wishlist. By calling::
   get_or_create_wishlist
the default wishlist for the current authenticated customer is created or 
retrieved from the database. This wishlist then becomes the active wishlist, and
normally each customer shall need only one of them.


If your shop shall offer more than one wishlist, add the following code to the

one wishlist can be active at a

Products may be added to

Contributing
============

Feel free to fork this project on github, send pull requests...
development discussion happends on the django SHOP mailing list
https://groups.google.com/forum/#!forum/django-shop
