from django.test import TestCase
from celery import shared_task
import requests
from .nova_poshta import request_status_order
from .models import Order, OrderStatus


@shared_task
def edit_consignment_note():
    orders = Order.objects.all()

    for order in orders:

        if order.order_status_id == 'Продажа' or order.consignment_note is None:
            pass

        else:
            request_status = request_status_order(consignment_note=order.consignment_note)

            if int(request_status) == 3:

                order.order_status_id = OrderStatus.objects.get(title='Заказ')
                # order.order_status_id = OrderStatus.objects.filter(title='Заказ').exists()
                order.save()

            elif int(request_status) == 1:
                order.order_status_id = OrderStatus.objects.get(title='Заказ')
                order.save()

            elif int(request_status) in (4, 5, 6, 7, 8, 14, 101):
                order.order_status_id = OrderStatus.objects.get(title='Доставка')
                order.save()

            elif int(request_status) in (9, 10, 11, 106):
                order.order_status_id = OrderStatus.objects.get(title='Продажа')
                order.save()

            elif int(request_status) in (102, 103, 108):
                order.order_status_id = OrderStatus.objects.get(title='Отказ')
                order.save()

            else:
                pass
