from rest_framework import serializers

from .models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=60)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['address', 'positions']

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)

        # здесь вам надо заполнить связанные таблицы
        StockProduct.objects.bulk_create([StockProduct(stock=stock,
                                                       product=position['product'],
                                                       quantity=position['quantity'],
                                                       price=position['price']) for position in positions])
        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        from rest_framework import serializers

        from .models import Product, StockProduct, Stock

        class ProductSerializer(serializers.ModelSerializer):
            title = serializers.CharField(max_length=60)

            class Meta:
                model = Product
                fields = ['id', 'title', 'description']

        class ProductPositionSerializer(serializers.ModelSerializer):

            class Meta:
                model = StockProduct
                fields = ['product', 'quantity', 'price']

        class StockSerializer(serializers.ModelSerializer):
            positions = ProductPositionSerializer(many=True)

            class Meta:
                model = Stock
                fields = ['address', 'positions']

            def validate_positions(self, value):
                if not value:
                    raise serializers.ValidationError('Не указаны позиции товара на складе')
                position_ids = [item['product'].id for item in value]
                if len(position_ids) != len(set(position_ids)):
                    raise serializers.ValidationError('Дублируются позиции товара на складе')
                return value

            def create(self, validated_data):
                positions = validated_data.pop('positions')
                stock = super().create(validated_data)
                StockProduct.objects.bulk_create([StockProduct(stock=stock,
                                                               product=position['product'],
                                                               quantity=position['quantity'],
                                                               price=position['price']) for position in positions])
                return stock

            def update(self, instance, validated_data):
                positions = validated_data.pop('positions')
                stock = super().update(instance, validated_data)
                for position in positions:
                    product = position.pop('product')
                    obj, created = StockProduct.objects.update_or_create(product=product, stock=stock,
                                                                         defaults=position)
                return stock
