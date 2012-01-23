======================================
Implementing wishlists for django-shop
======================================

Abstract
--------
Many Internet shop systems offer their customers a so called wishlist, so that
they can remember items they are interested in, for later acquisition. These
items are stored together with their user profile. When the customer visits the
shop at a later time, he can add one or more of these items to the shopping cart.

Introduction
------------
A shopping cart and a wishlist behave in a similar manner. The biggest
difference is, that a wishlist does only contain the kind of product, but not
its quantity. Therefore a wishlist only remembers, if a certain product was
added or not and behaves more like a tailor-made shop category.

In contrast to carts, where each customer has exactly one active cart, there is
a one-to-many relationship between each customer and his wishlists. The first
wishlist gets a default name, say “My wishlist”. For each additional wishlist,
the customer can choose a different name. There is no need to constrain the
names of wishlists to be unique.

For each product displayed in the shops detail view, the customer may add the
product to the wishlist using a button, similar to that of adding it to the
shopping chart.

In the view of his wishlist, each product description offers a button to remove
the item.
Product variations must honor wishlists and must therefore implement a table
remembering each customers choice for the given wishlist. Otherwise the base
product is remembered by the wishlist, but product options are misremembered.

Implementation problems
-----------------------
In the detail view of a product, an additional button has to be added. Clicking
on this button shall add the item to the wishlist. In the current sample
templates of a products detail view, no such additional button can be added,
because clicking on “Add to cart” invokes the cart view through the form action.
I therefore adjusted to form action for the product’s detail view to invoke a
post method in the class ProductDetailView. This method then will add the 
product to a cart or to a wishlist. Afterwards it will redirect the user onto
the list view for products.

The next problem is, that this method does not work well together with 
‘shop_simplevariations’. This module handles variations of products, but in
order to remember the variations in the cart extra functionality and tables 
(shop_simplevariations_cartitemoption, shop_simplevariations_cartitemtextoption)
have to be added. Since wishlists are similar, this functionality would have to 
be added as well.

I also do not like the idea, that a Product model must know how to implement
carts and other container objects such as wishlists. 

Proposal to handle these issues
-------------------------------
The database model for CartItem shall offer an additional field to store a
serialized representation of each concrete product variation. Other container 
objects such as OrderItem and WishlistItem shall also contain such an additional
field. Therefore a product variation can be transferred very easily between a
Wishlist, a Cart and an Order. As an additional benefit, there is no need for
tables such as shop_simplevariations_cartitemoption and 
shop_simplevariations_cartitemtextoption.
On the other side, it may become more difficult to search for a certain
variation in those tables, but personally I don’t see any use case for such a
search.

Since product variations are inextricably linked to their product, the
functionality to serialize and deserialize the concrete product variations has
to be added to the product model. This means that in the admin view, the
assignment of product variations now becomes part of the product details. When
using django-shop-simplevariations, product variations have to be assigned to
their product which is the other way round, but that’s a matter of taste.

One point of discussion is the format used to serialize the product variation. 
The first implementation used “Python pickle”, since session data is also 
serialized using this format. But as Chris Glass pointed out, in comparison to
session data, product variations in Order and Wishlist shall “survive” a
software upgrade, thus pickling the variation does not work. Therefore the
current implementation uses JSON, which is a simple and well understood
serializing format.
