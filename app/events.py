from flask import request
from flask_socketio import emit

from .extensions import socketio
from .models.Menu_Controller import MenuController
from .models.Order_Controller import OrderController
from .models.Order_Controller import Order
menu_controller = MenuController()
menu_controller.set_menu(1)
order_controller = OrderController()

print("events - menu-controller:",menu_controller.menu)

@socketio.on("connect")
def handle_connect():
    print("Client connected!")

#cliente
@socketio.on("send-menu")
def handle_order():
    emit('receive-menu', menu_controller.menu, broadcast=True)
    print("Se envio el menu")

#administrador

#estos dos son de ejemplo
users = {}
@socketio.on("user_join")
def handle_user_join(username):
    print(f"User {username} joined!")
    users[username] = request.sid

@socketio.on("new_message")
def handle_new_message(message):
    print(f"New message: {message}")
    username = None 
    for user in users:
        if users[user] == request.sid:
            username = user
    emit("chat", {"message": message, "username": username}, broadcast=True)
@socketio.on('handle-order')
def handle_order(order_data):
    # Extraer los detalles de la orden
    msg = order_data.get('msg')
    dishes = order_data.get('dishes', [])
    
    order = Order(order_controller.current_order_id, msg)
    order_controller.current_order_id += 1

    for dish_data in dishes:
        dish = {
            'dishId': dish_data.get('dishId'),
            'name': dish_data.get('name'),
            'status': 'order waiting'
        }
        order.add_dish(dish)

    

    order_controller.add_order(order)#Añadir a la cola
    print(type(order_controller.to_json()))
    emit('order-updated', order_controller.to_json(), broadcast=True)
    
    #emit('orderStatusChanged', order.__dict__, broadcast=True) #Emit

@socketio.on('updateOrderStatus')
def update_order_status(data):
    order_id = data['orderId']
    dishes = data['dishes']

    # OBtener la orden
    order = order_controller.get_order_by_id(order_id)
    if order:
        for dish in dishes:
            dish_id = dish['dishId']
            estado = dish['estado']

            # Encontrar la orden
            target_dish = next((d for d in order.dishes if d['dishId'] == dish_id), None)
            if target_dish:
                target_dish['estado'] = order.status

                if estado == 'order in process':
                    order.remove_dish(target_dish)

        # Emit event to update the order status
        emit('orderStatusChanged', order.__dict__, broadcast=True)

        # Move the order to the next phase if all dishes are in process
        if all(dish['estado'] == 'order in process' for dish in order.dishes):
            order.update_status('order ready')
            emit('orderStatusChanged', order.__dict__, broadcast=True)
