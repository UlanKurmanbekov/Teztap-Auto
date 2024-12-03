from django.db import models

from users.models import User


class CarMake(models.Model):
    name = models.CharField(verbose_name='Марка', max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Марка'
        verbose_name_plural = 'Марки'


class CarBody(models.Model):
    name = models.CharField(verbose_name='Кузов', max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Кузов'
        verbose_name_plural = 'Кузова'


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('processing', 'В процессе'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='Заказчик')
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, verbose_name='Марка')
    car_model = models.CharField(max_length=255, verbose_name='Модель')
    car_body = models.ForeignKey(CarBody, on_delete=models.CASCADE, verbose_name='Кузов')
    car_year = models.CharField(max_length=4, verbose_name='Год автомобиля')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    second_phone = models.CharField(max_length=255, verbose_name='Второй номер телефона')
    sample = models.ImageField(verbose_name='Образец', upload_to='sample/', null=True, blank=True)
    vin_code = models.CharField(verbose_name='VIN код', max_length=255)
    tech_passport = models.ImageField(upload_to='tech_passport/', verbose_name='Тех. пасспорт', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    def __str__(self):
        return f'Заказ №{self.id}: {self.user}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderImage(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(verbose_name='Фото', upload_to='order-images/')


class OrderPrice(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='price')
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Себестоимость')
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена продажи')

    class Meta:
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'

    def __str__(self):
        return f'Цена для заказа №{self.order.id}'
