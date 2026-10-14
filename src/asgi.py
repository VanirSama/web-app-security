from asgiref.wsgi import WsgiToAsgi

from src.app import app as flask_app

application = WsgiToAsgi(flask_app)