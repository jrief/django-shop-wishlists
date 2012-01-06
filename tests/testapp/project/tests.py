# -*- coding: utf-8 -*-
from decimal import Decimal
from django.test import TestCase
from django.core import exceptions
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from shop_wishlists.models import Wishlist, WishlistItem 
from shop_wishlists.utils import get_or_create_wishlist, is_product_on_active_wishlist, \
        rename_active_wishlist, delete_active_wishlist
from shop.tests.util import Mock
from project.models import DiaryProduct
from project.views import DiaryDetailView


class WishlistsTest(TestCase):    
    def setUp(self):
        self.request = Mock()
        setattr(self.request, 'session', {})
        self.user = User.objects.create(username="test",
                                        email="test@example.com",
                                        first_name="Test",
                                        last_name="Tester")
        self.product = DiaryProduct(isbn='1234567890', number_of_pages=100)
        self.product.name = 'test'
        self.product.slug = 'test'
        self.product.short_description = 'test'
        self.product.long_description = 'test'
        self.product.unit_price = Decimal('1.0')
        self.product.save()

    def test_get_templates_return_expected_values(self):
        view = DiaryDetailView()
        setattr(view, 'object', None)
        tmp = view.get_template_names()
        self.assertEqual(len(tmp), 1)

    def test_create_no_anonymous_wishlist(self):
        """Wishlists for anonymous users are not allowed"""
        setattr(self.request, 'user', None)
        self.assertRaises(exceptions.PermissionDenied, get_or_create_wishlist, self.request)
                          #wishlist, getattr(self.request, '_wishlist'))

    def test_create_wishlist(self):
        """Asking for a wishlist twice, shall create only one"""
        setattr(self.request, 'user', self.user)
        wishlist = get_or_create_wishlist(self.request)

        # check that wishlist is stored in request
        self.assertEqual(wishlist, get_or_create_wishlist(self.request))
        self.assertTrue(hasattr(self.request, '_wishlist'))
        self.assertTrue(self.request.session.has_key('active_wishlist'))

        # check that wishlist is stored in session
        request = Mock()
        setattr(request, 'session', {'active_wishlist': wishlist.id})
        setattr(request, 'user', self.user)
        self.assertEqual(wishlist, get_or_create_wishlist(request))

        # check that wishlist is stored for current user
        request = Mock()
        setattr(request, 'session', {})
        setattr(request, 'user', self.user)
        self.assertEqual(wishlist, get_or_create_wishlist(request))

    def test_do_not_share_wishlists(self):
        """"Different users shall never share a wishlist"""
        setattr(self.request, 'user', self.user)
        wishlist = get_or_create_wishlist(self.request)

        request = Mock()
        setattr(request, 'session', {})
        user2 = User.objects.create(username="test2", email="test2@example.com",
                                      first_name="Test2", last_name="Tester2")
        setattr(request, 'user', user2)
        self.assertNotEqual(wishlist, get_or_create_wishlist(request))

    def test_is_product_on_active_wishlist(self):
        """A product IS on the wishlist independently of its variation"""
        setattr(self.request, 'user', self.user)
        wishlist = get_or_create_wishlist(self.request)
        wishlist.add_product(self.product, variation={'foo': 'bar'})
        self.assertTrue(is_product_on_active_wishlist(self.request, self.product))

    def test_find_product_on_active_wishlist(self):
        """Products added to the wishlist must be found again"""
        setattr(self.request, 'user', self.user)
        wishlist = get_or_create_wishlist(self.request)
        variation = {'foo': 'bar'}
        wishlist.add_product(self.product, variation=variation)
        self.assertEqual(len(wishlist.get_all_items()), 1)
        items = wishlist.find_item(self.product)
        self.assertEqual(len(items), 0)
        items = wishlist.find_item(self.product, variation=variation)
        self.assertEqual(len(items), 1)
        wishlist.add_product(self.product, variation={'foo': 'baz'})
        self.assertEqual(len(wishlist.get_all_items()), 2)
        wishlist.add_product(self.product)
        self.assertEqual(len(wishlist.get_all_items()), 3)

    def test_rename_wishlist(self):
        """Products added to the wishlist must be found again"""
        setattr(self.request, 'user', self.user)
        self.assertRaises(exceptions.ObjectDoesNotExist, rename_active_wishlist, self.request, 'DEF')
        wishlist = get_or_create_wishlist(self.request)
        self.assertEqual(wishlist.name, _('My wishlist'))
        rename_active_wishlist(self.request, 'ABC')
        self.assertEqual(wishlist.name, 'ABC')
        request = Mock()
        setattr(request, 'user', self.user)
        setattr(request, 'session', {'active_wishlist': wishlist.id})
        rename_active_wishlist(request, 'DEF')
        wishlist = get_or_create_wishlist(request)
        self.assertEqual(wishlist.name, 'DEF')

    def test_delete_wishlist(self):
        """Deleting a wishlist also deletes all its items"""
        setattr(self.request, 'user', self.user)
        self.assertRaises(exceptions.ObjectDoesNotExist, delete_active_wishlist, self.request)
        wishlist = get_or_create_wishlist(self.request)
        wishlist.add_product(self.product)
        self.assertEqual(WishlistItem.objects.filter(wishlist=wishlist).count(), 1)
        self.assertEqual(Wishlist.objects.all().count(), 1)
        request = Mock()
        setattr(request, 'user', self.user)
        setattr(request, 'session', {'active_wishlist': wishlist.id})
        delete_active_wishlist(request)
        self.assertFalse(hasattr(request, '_wishlist'))
        self.assertFalse(request.session.has_key('active_wishlist'))
        self.assertEqual(Wishlist.objects.all().count(), 0)
        # check for automatic delete cascade
        self.assertEqual(WishlistItem.objects.filter(wishlist=wishlist).count(), 0)
        get_or_create_wishlist(request)
        self.assertEqual(Wishlist.objects.all().count(), 1)
        delete_active_wishlist(request)
        self.assertEqual(Wishlist.objects.all().count(), 0)
