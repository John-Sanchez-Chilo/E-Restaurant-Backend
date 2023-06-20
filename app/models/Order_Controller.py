
from collections import deque
from ..extensions import SocketIO,emit
import json

class Order:
    def __init__(self, order_id, msg):
        self.order_id = order_id
        self.msg = msg
        self.status = 'order waiting'
        self.dishes = []

    def add_dish(self, dish):
        self.dishes.append(dish)

    def remove_dish(self, dish):
        self.dishes.remove(dish)

    def update_status(self, status):
        self.status = status
class OrderEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Order):
            return {
                'order_id': obj.order_id,
                'msg': obj.msg,
                'status': obj.status,
                'dishes': obj.dishes
            }
        return super().default(obj)
class OrderController:
    def __init__(self):
        self.order_queue = deque()
        self.current_order_id = 1

    def add_order(self, order):
        self.order_queue.append(order)
    def get_order_queue(self):
        return list(self.order_queue)
    def remove_order(self, order):
        self.order_queue.remove(order)

    def get_order_by_id(self, order_id):
        for order in self.order_queue:
            if order.order_id == order_id:
                return order
        return None
    def to_json(self):
        return json.dumps(self.get_order_queue(), cls=OrderEncoder)
