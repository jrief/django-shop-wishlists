# -*- coding: utf-8 -*-
from shop.views import ShopDetailView
from shop_productvariations.views import ProductDetailViewMixin as VariationProductMixin
from models import DiaryProduct


class DiaryDetailView(VariationProductMixin, ShopDetailView):
    """
    This view handles displaying the detail view for test product Diary 
    """
    model = DiaryProduct
