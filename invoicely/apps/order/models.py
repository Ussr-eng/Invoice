from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime


class NPWarehouse(models.Model):

    title = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'


class OrderStatus(models.Model):

    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    created_by = models.ForeignKey(User, related_name='order_status', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'


class SourceOrder(models.Model):

    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    created_by = models.ForeignKey(User, related_name='source_order', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'


class PayoutStatus(models.Model):

    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    created_by = models.ForeignKey(User, related_name='payout_status', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'


class SourceTraffic(models.Model):

    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    created_by = models.ForeignKey(User, related_name='source_traffic', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'


class Provider(models.Model):

    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(User, related_name='created_provider', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'

    def count_orders(self):
        orders = Order.objects.filter(provider_id=self)

        return len([order.id for order in orders])

    def count_product(self):
        products = Product.objects.filter(provider=self)

        return len([product.title for product in products])

    def get_income_success_orders(self):
        orders = Order.objects.filter(provider_id=self.id, order_status_id__title='Продажа')

        return sum([order.income for order in orders])

    def get_success_orders(self):
        orders = Order.objects.filter(provider_id=self, order_status_id__title='Продажа')

        return len(orders)

    def get_unsuccess_orders(self):

        orders = Order.objects.filter(provider_id=self.id, order_status_id__title='Отказ')
        return len(orders)


class Product(models.Model):

    title = models.CharField(max_length=255)
    drop_price = models.IntegerField()
    sale_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    provider = models.ForeignKey(Provider, related_name='product', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'

    def get_provider_id(self):

        product = Product.objects.get(id=self.id)
        provider = Provider.objects.get(id=product.provider.id)

        return provider.id

    def get_provider(self):

        product = Product.objects.get(id=self.id)
        provider = Provider.objects.get(id=product.provider.id)

        return provider

    def income(self):

        return self.sale_price - self.drop_price

    def get_success_orders(self):
        try:
            order = Order.objects.filter(product_id=self.id, order_status_id__title='Продажа')
            return len(order)
        except:
            return 0

    def get_unsuccess_orders(self):
        try:
            order = Order.objects.filter(product_id=self.id, order_status_id__title='Отказ')
            return len(order)
        except:
            return 0


class ProductSize(models.Model):

    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    product = models.ForeignKey(Product, related_name='product_size', on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, related_name='product_size', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'


class Order(models.Model):

    name = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=255, blank=True, null=True)
    provider_id = models.ForeignKey(Provider, related_name='orders', on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, related_name='orders', on_delete=models.CASCADE)
    size = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    warehouse = models.CharField(max_length=255, blank=True, null=True)
    # ttn
    consignment_note = models.CharField(max_length=255, blank=True, null=True)
    settings_delivery = models.CharField(max_length=255, blank=True, null=True)
    prepayment = models.CharField(max_length=255, blank=True, null=True, default=0)
    cash_on_delivery = models.CharField(max_length=255, blank=True, null=True)
    income = models.IntegerField()
    source_order_id = models.ForeignKey(SourceOrder, related_name='orders', on_delete=models.CASCADE)
    source_traffic_id = models.ForeignKey(SourceTraffic, related_name='orders', on_delete=models.CASCADE)
    order_status_id = models.ForeignKey(OrderStatus, related_name='orders', on_delete=models.CASCADE)
    payout_status_id = models.ForeignKey(PayoutStatus, related_name='orders', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='created_orders', on_delete=models.CASCADE)
    modified_by = models.ForeignKey(User, related_name='modified_orders', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.created_at}'

    class Meta:
        ordering = ['-id']

    def get_date_formatted(self):
        return self.created_at.strftime("%d.%m %H:%M")
