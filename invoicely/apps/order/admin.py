from django.contrib import admin
from .models import Provider, Product, ProductSize, SourceOrder, SourceTraffic, OrderStatus, PayoutStatus, Order


admin.site.register(SourceTraffic)
admin.site.register(SourceOrder)
admin.site.register(OrderStatus)
admin.site.register(PayoutStatus)
admin.site.register(Provider)
admin.site.register(Product)
admin.site.register(ProductSize)
admin.site.register(Order)
