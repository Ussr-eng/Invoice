from rest_framework import serializers
from .models import Provider, Product, ProductSize, NPWarehouse, SourceOrder, SourceTraffic, OrderStatus, PayoutStatus,\
    Order


class NPWarehouseSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NPWarehouse
        read_only_fields = (
            "created_at",
        ),
        fields = (
            "id",
            "title",
        )


class SourceOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceOrder
        read_only_fields = (
            "created_at",
        ),
        fields = (
            "id",
            "title",
        )


class SourceTrafficSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceTraffic
        read_only_fields = (
            "created_at",
        ),
        fields = (
            "id",
            "title",
        )


class PayoutStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayoutStatus
        read_only_fields = (
            "created_at",
        ),
        fields = (
            "id",
            "title",
        )


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        read_only_fields = (
            "created_at",
        ),
        fields = (
            "id",
            "title",
        )


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        read_only_fields = (
            "product",
            "created_at",
        ),
        fields = (
            "id",
            "title",
        )


class SupportProductProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        read_only_fields = (
            "created_by",
            "created_at",
            "modified_at",

        ),
        fields = (
            "id",
            "title"
        )


class ProductSerializer(serializers.ModelSerializer):
    get_provider_id = serializers.CharField(required=False)
    income = serializers.IntegerField(required=False)
    get_success_orders = serializers.IntegerField(required=False)
    get_unsuccess_orders = serializers.IntegerField(required=False)

    class Meta:
        model = Product
        read_only_fields = (
            "created_at",
        ),
        fields = (
            "id",
            "title",
            "drop_price",
            "sale_price",
            "get_provider_id",
            "get_provider",
            "income",
            "get_success_orders",
            "get_unsuccess_orders",
        )

    def to_representation(self, instance):

        self.fields['get_provider'] = SupportProductProviderSerializer(read_only=True)

        return super(ProductSerializer, self).to_representation(instance)


class ProviderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True)
    count_orders = serializers.IntegerField(required=False)
    count_product = serializers.IntegerField(required=False)
    get_income_success_orders = serializers.IntegerField(required=False)
    get_success_orders = serializers.IntegerField(required=False)
    get_unsuccess_orders = serializers.IntegerField(required=False)

    class Meta:
        model = Provider
        read_only_fields = (
            "created_by",
            "created_at",
            "modified_at",
        ),
        fields = (
            "id",
            "title",
            "product",
            "count_orders",
            "count_product",
            "get_income_success_orders",
            "get_success_orders",
            "get_unsuccess_orders",
        )

    def create(self, validated_data):
        products_data = validated_data.pop('product')

        provider = Provider.objects.create(**validated_data)

        for product in products_data:
            Product.objects.create(provider=provider, **product)

        return provider


class OrderSerializer(serializers.ModelSerializer):
    income = serializers.IntegerField(required=False)

    class Meta:
        model = Order
        read_only_fields = (
            "created_by",
            "modified_by",
            "created_at",
            "modified_at",
        ),
        fields = (
            "id",
            "name",
            "telephone",
            "provider_id",
            "product_id",
            "size",
            "quantity",
            "city",
            "warehouse",
            "consignment_note",
            "settings_delivery",
            "prepayment",
            "cash_on_delivery",
            "source_order_id",
            "source_traffic_id",
            "payout_status_id",
            "order_status_id",
            "get_date_formatted",
            "income"
        )
        # depth = 1

    def to_representation(self, instance):

        self.fields['provider_id'] = ProviderSerializer(read_only=True)
        self.fields['product_id'] = ProductSerializer(read_only=True)
        self.fields['source_order_id'] = SourceOrderSerializer(read_only=True)
        self.fields['source_traffic_id'] = SourceTrafficSerializer(read_only=True)
        self.fields['payout_status_id'] = PayoutStatusSerializer(read_only=True)
        self.fields['order_status_id'] = OrderStatusSerializer(read_only=True)

        return super(OrderSerializer, self).to_representation(instance)
