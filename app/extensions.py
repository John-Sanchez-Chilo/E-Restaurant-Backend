from flask_socketio import SocketIO ,emit
from .models.connection_pool import MySQLPool

socketio = SocketIO(cors_allowed_origins='*')
mysql_pool = MySQLPool()

from .models.Menu import Menu
from .models.Menu_Item import MenuItem
from .models.Item import Item

menu_model = Menu()
menu_item_model = MenuItem()
item_model = Item()