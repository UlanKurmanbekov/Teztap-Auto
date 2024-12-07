from datetime import datetime

from rest_framework import serializers
from orders.models import Order, OrderImage


class OrderImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderImage
        fields = ['image']


class OrderSerializer(serializers.ModelSerializer):
    images = OrderImageSerializer(many=True, read_only=True)
    upload_images = serializers.ListField(child=serializers.ImageField(), write_only=True)
    vin_code = serializers.CharField(required=True)

    class Meta:
        model = Order
        fields = [
            'id', 'car_make_model',
            'car_year', 'car_body', 'vin_code', 'vin_image', 'status',
            'second_phone', 'images', 'upload_images', 'sample', 'tech_passport'
        ]

    def validate_upload_images(self, upload_images):
        if len(upload_images) > 6:
            raise serializers.ValidationError('Вы можете загрузить не более 10 изображений.')
        return upload_images

    def validate_vin_code(self, vin_code):
        if len(vin_code) != 17:
            raise serializers.ValidationError('VIN-код должен содержать 17 символов.')
        return vin_code

    def validate_car_year(self, car_year):
        current_year = datetime.now().year
        if not 1980 < int(car_year) < current_year:
            raise serializers.ValidationError(
                'Год автомобиля должен быть в диапазоне от 1980 до текущего года включительно'
            )
        return car_year

    def create(self, validated_data):
        images = validated_data.pop('upload_images', [])
        order = Order.objects.create(**validated_data)

        if images:
            order_images = [OrderImage(image=image, order=order) for image in images]
            OrderImage.objects.bulk_create(order_images)

        return order

    def update(self, instance, validated_data):
        images = validated_data.pop('upload_images', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if images is not None:
            instance.images.all().delete()
            order_images = [OrderImage(image=image, order=instance) for image in images]
            OrderImage.objects.bulk_create(order_images)

        return instance
