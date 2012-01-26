# -*- coding: utf-8 -*-
from shop.views.product import ProductDetailView
from shop_product_optiongroups.views import ProductOptionGroupsViewMixin
from shop_product_textoptions.views import ProductTextOptionsViewMixin
from models import DiaryProduct


class DiaryDetailView(ProductOptionGroupsViewMixin, \
                      ProductTextOptionsViewMixin, ProductDetailView):
    """
    This view handles displaying the detail view for test product Diary 
    """
    model = DiaryProduct
