import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'education_tracker.settings')

application = get_asgi_application()

import education_tracker.routing

application = ProtocolTypeRouter({
    "http": application,
    "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(education_tracker.routing.websocket_urlpatterns))
        ),
})
