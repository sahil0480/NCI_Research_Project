import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest_mgmt.settings')

application = get_wsgi_application()

# Correct root path for collected static files
BASE_DIR = Path(__file__).resolve().parent.parent
application = WhiteNoise(application, root=os.path.join(BASE_DIR, 'staticfiles'))
