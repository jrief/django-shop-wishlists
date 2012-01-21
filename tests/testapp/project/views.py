# -*- coding: utf-8 -*-
from shop.views.product import ProductDetailView
from shop_productvariations.views import ProductDetailViewMixin as VariationProductMixin
from models import DiaryProduct


class DiaryDetailView(VariationProductMixin, ProductDetailView):
    """
    This view handles displaying the detail view for test product Diary 
    """
    model = DiaryProduct
