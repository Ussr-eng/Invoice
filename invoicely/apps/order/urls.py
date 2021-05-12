from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProviderViewSet, ProductViewSet, ProductSizeViewSet, SourceTrafficViewSet, SourceOrdersViewSet, \
    OrderStatusViewSet, PayoutStatusViewSet, OrderViewSet, generate_pdf_only

router = DefaultRouter()
router.register("providers", ProviderViewSet, basename="providers")
router.register("products", ProductViewSet, basename="products")
router.register("products_size", ProductSizeViewSet, basename="products_size")
router.register("source_traffic", SourceTrafficViewSet, basename="source_traffic")
router.register("source_orders", SourceOrdersViewSet, basename="source_orders")
router.register("order_status", OrderStatusViewSet, basename="order_status")
router.register("payout_status", PayoutStatusViewSet, basename="payout_status")
router.register("orders", OrderViewSet, basename="orders")


urlpatterns = [
    path('', include(router.urls)),
    path('order/<int:order_id>/generate_pdf_only', generate_pdf_only, name='generate_pdf_only'),
    # path('nowa_poshta/', nowa_poshta, name='nowa_poshta'),
    # path('order/get_all_warehouse/', get_all_warehouse, name='get_all_warehouse')
]
