from django.db import models

from users.models import User
from orders.models import Order


class Notification(models.Model):
    recipient = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='notifications',
        null=True,
        on_delete=models.CASCADE
    )
    order = models.ForeignKey(Order, verbose_name='Заказ', related_name='notifications', on_delete=models.CASCADE)
    message = models.CharField(verbose_name='Сообщение', max_length=255)
    is_read = models.BooleanField(verbose_name='Прочитано', default=False)
    created_at = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Изменен', auto_now=True)

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'

    def __str__(self):
        return f'{self.message} {self.order}'
