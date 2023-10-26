from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.template.loader import get_template

user_connections = {}

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            self.accept()
            group_name = f"user-notifications-{self.user.id}"
            self.channel_layer.group_add(group_name, self.channel_name)

    def disconnect(self, close_code):
        group_name = f"user-notifications-{self.user.id}"
        self.channel_layer.group_discard(group_name, self.channel_name)

    def send_assignment_notification(self, recipient, assignment_message):
        # Send an assignment notification to the specified recipient
        message = f'New Indicator Assignment: {assignment_message}'
        event = {
            'type': 'send_user_notification',
            'message': message
        }
        recipient_channel_name = user_connections.get(recipient.id)
        if recipient_channel_name:
            async_to_sync(self.channel_layer.send)(recipient_channel_name, event)