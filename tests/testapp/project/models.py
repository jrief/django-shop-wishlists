# -*- coding: utf-8 -*-
from django.db import models
from shop.models.productmodel import Product
from shop_product_optiongroups.models import ProductOptionGroupsMixin
from shop_product_textoptions.models import ProductTextOptionsMixin


class DiaryProduct(Product, ProductOptionGroupsMixin, ProductTextOptionsMixin):
    isbn = models.CharField(max_length=255)
    number_of_pages = models.IntegerField()
