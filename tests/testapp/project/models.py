# -*- coding: utf-8 -*-
from django.db import models
from shop_productvariations.models import VariableProduct


class DiaryProduct(VariableProduct):
    isbn = models.CharField(max_length=255)
    number_of_pages = models.IntegerField()
