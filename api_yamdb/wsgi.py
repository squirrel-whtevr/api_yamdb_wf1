"""
WSGI config for YaMDb project.
<<<<<<< HEAD

It exposes the WSGI callable as a module-level variable named ``application``.

=======
It exposes the WSGI callable as a module-level variable named ``application``.
>>>>>>> titles
For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')

application = get_wsgi_application()
