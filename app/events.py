from flask import request
from flask_socketio import emit

from .extensions import socketio
from .models.Menu_Controller import MenuController
from .models.Order_Controller import OrderController
from .models.Order_Controller import Order

menu_controller = MenuController()
order_controller = OrderController()

@socketio.on("connect")
def handle_connect():
    print("Client connected!")

#cliente
@socketio.on("send-menu")
def send_menu():
    emit('receive-menu', menu_controller.menu, broadcast=True)
    print("Se envio el menu")

@socketio.on("get-ready-menu")
def get_ready_menu():
    emit('get-ready-menu', menu_controller.get_ready_menu(), broadcast=True)
    print("Se envio el menu listo")



#administrador

@socketio.on("get-complete-menu")
def get_complete_menu():
    emit('get-complete-menu', menu_controller.get_complete_menu(), broadcast=True)
    print("Se envio el menu completo")

@socketio.on("get-menus")
def get_menus():
    emit('get-menus', menu_controller.get_menus(), broadcast=True)
    print("Se envio los menus")

@socketio.on("set-menu")
def set_menu(menu):
    menu_controller.set_actual_menu(menu)
    emit('get-complete-menu',menu_controller.get_complete_menu() , broadcast=True)
    print("Se actualizo los menus")

@socketio.on("enable-item")
def enable_item(item):
    print("socket enable",item)
    menu_controller.enable_item(item['id_item'], item['amount'])
    emit('get-item-from-ready-menu', item , broadcast=True)
    print("Se habilito un item")

@socketio.on("disable-item")
def disable_item(item):
    menu_controller.disable_item(item)
    #emit('get-complete-item',menu_controller.get_complete_item() , broadcast=True)
    print("Se deshabilito un item")


@socketio.on("get-items-from-menu")
def get_menus(id_menu):
    emit('get-items-from-menu', menu_controller.get_all_items_from_menu(id_menu), broadcast=True)
    print("Se envio los menus")

@socketio.on("handle-menu")
def handle_menu(menu):
    menu_controller.set_menu(menu)
    emit('receive-menu', menu_controller.get_menu_items(), broadcast=True)
    print("Se recibio el menu")

@socketio.on("send-menu")
def send_menu():
    emit('receive-menu', menu_controller.get_menu_items(), broadcast=True)
    print("Se envio el menu al cliente")


@socketio.on("handle-order")
def handle_order(order):
    #esta orden debe ser almacenada
    emit('send-order', order, broadcast=True)
    print("Se recibio y envio la orden")

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
    
    
#levi
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
