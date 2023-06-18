from flask_socketio import SocketIO 
from .models.connection_pool import MySQLPool
socketio = SocketIO(cors_allowed_origins='*')
mysql_pool = MySQLPool()