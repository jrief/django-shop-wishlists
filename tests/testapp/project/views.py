# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from shop_productvariations.views import VariableProductDetailView
from models import DiaryProduct


class DiaryDetailView(VariableProductDetailView):
    """
    This view handles displaying the detail view for test product Diary 
    """
    model = DiaryProduct
