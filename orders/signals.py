from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

from .models import Order
from notifications.models import Notification


@receiver(pre_save, sender=Order)
def capture_previous_status(sender, instance, **kwargs):
    if instance.pk:
        previous = Order.objects.get(pk=instance.pk)
        instance._previous_status = previous.status


@receiver(post_save, sender=Order)
def create_notification_on_status_change(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.user,
            order=instance,
            message='Заказ ожидает обработки'
        )
    else:
        MESSAGES = {
            'pending': 'Заказ в повторной обработке',
            'processing': 'Заказ в процессе обработки',
            'completed': 'Заказ завершен',
            'cancelled': 'Заказ отменен',
        }
        if hasattr(instance, '_previous_status'):
            previous_status = instance._previous_status
            if previous_status != instance.status:
                Notification.objects.create(
                    recipient=instance.user,
                    order=instance,
                    message=MESSAGES[instance.status],
                )
