from django.shortcuts import render
import pdfkit
from django.core.exceptions import PermissionDenied
from django.core import serializers
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from datetime import timedelta, datetime, date
from django.utils import timezone


from .nova_poshta import request_status_order

from rest_framework import viewsets, status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes, action
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from .service import PaginationOrders

from .models import Provider, ProductSize, Product, NPWarehouse, OrderStatus, SourceTraffic, SourceOrder, PayoutStatus,\
    Order
from .serializers import ProviderSerializer, ProductSerializer, ProductSizeSerializer, SourceOrderSerializer, \
    SourceTrafficSerializer, PayoutStatusSerializer, OrderStatusSerializer, OrderSerializer


class ProviderViewSet(viewsets.ModelViewSet):
    serializer_class = ProviderSerializer
    queryset = Provider.objects.all()

    @action(detail=False, methods=['post', 'get'])
    def data_for_main_page(self, request):

        products = Provider.objects.filter(created_by=request.user)

        serializer = ProviderSerializer(products, many=True)
        return Response([serializer.data], status=status.HTTP_200_OK)

    def get_queryset(self):

        return self.queryset.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):

        obj = self.get_object()

        if self.request.user != obj.created_by:
            raise PermissionDenied('Wrong object owner')

        serializer.save()


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    @action(detail=False, methods=['post', 'get'])
    def data_for_main_page(self, request):

        products = Product.objects.filter(provider__created_by=request.user)

        serializer = ProductSerializer(products, many=True)
        return Response([serializer.data], status=status.HTTP_200_OK)

    @action(detail=False, methods=['post', 'get'])
    def edit_price(self, request):

        product = Product.objects.get(id=request.data['id'])
        product.drop_price = request.data['drop_price']
        product.sale_price = request.data['sale_price']
        try:
            product.title = request.data['title']
        except:
            pass
        product.save()

        response = {'message': 'price has been updater'}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post', 'get'])
    def create_product(self, request, pk=None):

        provider = Provider.objects.get(pk=pk)
        product = Product.objects.create(title=request.data['title'],
                                         drop_price=request.data['drop_price'],
                                         sale_price=request.data['sale_price'],
                                         provider=provider)

        return Response(status=status.HTTP_200_OK)

    def get_queryset(self):

        # print([product.get_provider().__dict__['title'] for product in self.queryset])
        # print([product.get_provider() for product in self.queryset])

        if self.request.GET.get('provider_id'):

            provider_id = self.request.GET.get('provider_id', 0)

            return self.queryset.filter(provider__id=provider_id)

        elif self.request.GET.get('product_id'):

            # product = [item.get_provider().__dict__ for item in query][0]
            # provider = [item.__dict__ for item in query][0]
            # print(self.queryset.filter(id=self.request.GET.get('product_id'))[0].get_provider())

            return self.queryset.filter(id=self.request.GET.get('product_id'))

    def perform_create(self, serializer):

        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):

        obj = self.get_object()

        if self.request.user != obj.created_by:
            raise PermissionDenied('Wrong object owner')

        serializer.save()


class ProductSizeViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSizeSerializer
    queryset = ProductSize.objects.all()

    def get_queryset(self):

        if self.request.GET.get('product_id'):

            return self.queryset.filter(product__id=self.request.GET.get('product_id'))


class SourceTrafficViewSet(viewsets.ModelViewSet):
    serializer_class = SourceTrafficSerializer
    queryset = SourceTraffic.objects.all()

    @action(detail=False, methods=['post', 'get'],)
    def set_default(self, request):
        array = ['Instagram', 'OLX', 'Facebook', 'adwords', 'Яндекс.Директ', 'Organic', 'direct']
        count = 0

        while 6 >= count:
            traffic = SourceTraffic.objects.create(title=array[count], created_by=request.user)
            count += 1

        traffic_all = SourceTraffic.objects.all()
        serializer = SourceTrafficSerializer(traffic_all, many=True)
        return Response([serializer.data], status=status.HTTP_200_OK)

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):

        obj = self.get_object()

        if self.request.user != obj.created_by:
            raise PermissionDenied('Wrong object owner')

        serializer.save()


class SourceOrdersViewSet(viewsets.ModelViewSet):
    serializer_class = SourceOrderSerializer
    queryset = SourceOrder.objects.all()

    @action(detail=False, methods=['post', 'get'])
    def set_default(self, request):
        array = ['Instagram', 'OLX', 'Facebook', 'Prom', 'Rozetka', 'Vk', 'Сайт']
        count = 0

        while 6 >= count:
            traffic = SourceOrder.objects.create(title=array[count], created_by=request.user)
            count += 1

        source_order_all = SourceTraffic.objects.all()
        serializer = SourceTrafficSerializer(source_order_all, many=True)
        return Response([serializer.data], status=status.HTTP_200_OK)

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):

        obj = self.get_object()

        if self.request.user != obj.created_by:
            raise PermissionDenied('Wrong object owner')

        serializer.save()


class OrderStatusViewSet(viewsets.ModelViewSet):
    serializer_class = OrderStatusSerializer
    queryset = OrderStatus.objects.all()

    @action(detail=False, methods=['post', 'get'])
    def set_default(self, request):
        array = ['Заказ', 'Доставка', 'Продажа', 'Отказ']
        count = 0

        while 3 >= count:
            traffic = OrderStatus.objects.create(title=array[count], created_by=request.user)
            count += 1

        status_order_all = OrderStatus.objects.all()
        serializer = OrderStatusSerializer(status_order_all, many=True)
        return Response([serializer.data], status=status.HTTP_200_OK)

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):

        obj = self.get_object()

        if self.request.user != obj.created_by:
            raise PermissionDenied('Wrong object owner')

        serializer.save()


class PayoutStatusViewSet(viewsets.ModelViewSet):
    serializer_class = PayoutStatusSerializer
    queryset = PayoutStatus.objects.all()

    @action(detail=False, methods=['post', 'get'])
    def set_default(self, request):
        array = ['Выплачено', 'Не выплачено']
        count = 0

        while 1 >= count:
            traffic = PayoutStatus.objects.create(title=array[count], created_by=request.user)
            count += 1

        payout_status_all = PayoutStatus.objects.all()
        serializer = PayoutStatusSerializer(payout_status_all, many=True)
        return Response([serializer.data], status=status.HTTP_200_OK)

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):

        obj = self.get_object()

        if self.request.user != obj.created_by:
            raise PermissionDenied('Wrong object owner')

        serializer.save()


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    pagination_class = PaginationOrders

    @action(detail=False, methods=['POST', 'GET'])
    def get_orders_by_providers_date(self, request):
        pagination = PaginationOrders()

        print(len(request.data))
        print(request.data)

        if len(request.data) == 1:

            if request.data.get('date'):

                orders = Order.objects.filter(created_by=request.user,
                                              created_at__contains=request.data['date'])

            elif request.data.get('provider_id'):

                orders = Order.objects.filter(created_by=request.user,
                                              provider_id=request.data['provider_id'])

            elif request.data.get('status_order'):

                orders = Order.objects.filter(created_by=request.user,
                                              order_status_id__title=request.data['status_order'])

        elif len(request.data) == 2:

            if request.data.get('date') and request.data.get('provider_id'):

                orders = Order.objects.filter(created_by=request.user,
                                              provider_id=request.data['provider_id'],
                                              created_at__contains=request.data['date'])

            elif request.data.get('date') and request.data.get('status_order'):

                orders = Order.objects.filter(created_by=request.user,
                                              order_status_id__title=request.data['status_order'],
                                              created_at__contains=request.data['date'])

            elif request.data.get('provider_id') and request.data.get('status_order'):

                orders = Order.objects.filter(created_by=request.user,
                                              order_status_id__title=request.data['status_order'],
                                              provider_id=request.data['provider_id'])

        elif len(request.data) == 3:

            orders = Order.objects.filter(created_by=request.user,
                                          created_at__contains=request.data['date'],
                                          order_status_id__title=request.data['status_order'],
                                          provider_id=request.data['provider_id'])

        else:

            orders = Order.objects.filter(created_by=request.user)

        pagination.page_size = 13
        result_page = pagination.paginate_queryset(orders, request)
        serializer = OrderSerializer(result_page, many=True)
        return pagination.get_paginated_response(serializer.data)

    @action(detail=False, methods=['POST', 'GET'])
    def get_orders_total_data(self, request):

        if len(request.data) == 0:

            orders = Order.objects.filter(created_by=request.user)

        else:
            try:
                if int(request.data['date']) in [7, 14, 30]:

                    orders = Order.objects.filter(
                        created_by=request.user,
                        created_at__range=(timezone.now() - timedelta(days=int(request.data['date'])), timezone.now()))

                    print(list(order for order in orders))

            except:
                # TODO use try except if in request empty list

                orders = Order.objects.filter(created_by=request.user, created_at__contains=request.data['date'])

        count_orders = {'count_orders': len(orders)}
        successful = {'successful':
                      len([order for order in orders if order.order_status_id.__dict__['title'] == 'Продажа'])}
        unsuccessful = {'unsuccessful':
                        len([order for order in orders if order.order_status_id.__dict__['title'] == 'Отказ'])}
        sum_of_all_orders = {'sum_of_all_orders': sum([order.product_id.sale_price for order in orders
                                                       if order.order_status_id.__dict__['title'] == 'Продажа'])}

        sum_income = {'income': sum([order.income for order in orders
                                    if order.order_status_id.__dict__['title'] == 'Продажа'])}

        average_profit_per_order = {'average_profit_per_order': int(sum([order.income for order in orders
                                    if order.order_status_id.__dict__['title'] == 'Продажа']) /

                                    len([order.income for order in orders
                                        if order.order_status_id.__dict__['title'] == 'Продажа']) if
                                    len([order.income for order in orders
                                        if order.order_status_id.__dict__['title'] == 'Продажа']) else 0)
                                    }

        return Response({**sum_income, **count_orders, **sum_of_all_orders, **successful, **unsuccessful,
                         **average_profit_per_order},
                        status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST', 'GET'])
    def edit_consignment_note(self, request, pk=None):

        order = Order.objects.get(pk=pk)

        order.consignment_note = request.data["consignment_note"]
        order.save()

        serializer = OrderSerializer(Order.objects.get(pk=pk), many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)

    def perform_create(self, serializer):

        get_product = serializer.validated_data.get('product_id')
        income = get_product.__dict__['sale_price'] - get_product.__dict__['drop_price']

        serializer.save(created_by=self.request.user,
                        modified_by=self.request.user,
                        income=income)

    def perform_update(self, serializer):

        obj = self.get_object()

        if self.request.user != obj.created_by:
            raise PermissionDenied('Wrong object owner')

        serializer.save()


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def generate_pdf_only(request, order_id):

    order = get_object_or_404(Order, pk=order_id, created_by=request.user)

    template_name = 'pdf_1.html'
    template = get_template(template_name)
    html = template.render({'order': order})
    pdf = pdfkit.from_string(html, False, options={})

    response = HttpResponse(pdf, content_type='aplication/pdf')
    response['Content-Dispositions'] = 'attachment; filename="order.pdf"'

    return response
