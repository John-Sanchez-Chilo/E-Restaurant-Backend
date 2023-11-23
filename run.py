from app import create_app, socketio
from test import suite
import unittest

app = create_app()

socketio.run(app)

#runner = unittest.TextTestRunner()
#runner.run(suite())