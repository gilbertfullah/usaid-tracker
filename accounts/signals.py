from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from accounts.models import Assignment, Notification
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Assignment)
def send_notification_on_assignment(sender, instance, created, **kwargs):
    if created and instance.assigned_to:
        recipient = instance.assigned_to
        message = f'You have a new indicator assigned: {instance.indicator.name}'
        Notification.objects.create(user=recipient, message=message)

        # Send a WebSocket message to the user
        channel_layer = get_channel_layer()
        group_name = f"user-notifications-{recipient.id}"
        event = {
            'type': 'send_notification',
            'message': message,
        }

        async_to_sync(channel_layer.group_send)(group_name, event)

        logger.info(f"Notification sent to {recipient.username}: {message}")
