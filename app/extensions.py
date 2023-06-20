from flask_socketio import SocketIO ,emit
from .models.connection_pool import MySQLPool
socketio = SocketIO(cors_allowed_origins='*')
mysql_pool = MySQLPool()