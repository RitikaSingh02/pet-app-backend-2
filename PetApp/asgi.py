# import os
# import django
# from channels.routing import get_default_application
# # from django.core.asgi import get_asgi_application
# # import channels.layers
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PetApp.settings')

# application = get_default_application()
# django.setup()
# # channel_layer = channels.layers.get_channel_layer()

import os
import django
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PetApp.settings")
django.setup()
application = get_default_application()
