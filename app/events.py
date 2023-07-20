from flask import request
from flask_socketio import emit

from .extensions import socketio
from .models.Menu_Controller import MenuController
from .models.Order_Controller import OrderController
from .models.Order_Controller import Order
from .models.Frequency_Controller import FrequencyController
menu_controller = MenuController()
order_controller = OrderController()
frequency_controller = FrequencyController()
#administrador
#MenuView
@socketio.on("get-complete-menu")
def get_complete_menu():
    #print("Evento: get-complete-menu", menu_controller.get_complete_menu())
    emit('get-complete-menu', menu_controller.get_complete_menu(), broadcast=True)

@socketio.on("get-menus")
def get_menus():
    print("Evento: get-menus")
    emit('get-menus', menu_controller.get_menus(), broadcast=True)

@socketio.on("set-menu")
def set_menu(menu):
    print("Evento: set-menu")
    current_menu = menu_controller.set_actual_menu(menu)
    frequency_controller.set_items(current_menu['items'])
    print("Frequency controller",frequency_controller.get_list_of_frequency())
    emit('get-complete-menu',menu_controller.get_complete_menu() , broadcast=True)
    emit('set-frequency', frequency_controller.get_list_of_frequency(), broadcast=True)

@socketio.on("enable-item")
def enable_item(item):
    print("Evento: enable-item")
    menu_controller.enable_item(item['id_item'], item['amount'])
    item['amount'] = 0
    emit('add-item-to-ready-menu', item , broadcast=True)

@socketio.on("disable-item")
def disable_item(item):
    print("Evento: disable-item")
    menu_controller.disable_item(item)
    #emit('get-complete-item',menu_controller.get_complete_item() , broadcast=True)

#Cliente
@socketio.on("get-ready-menu")
def get_ready_menu():
    print("Evento: get-ready-menu")
    emit('get-ready-menu', menu_controller.get_ready_menu(), broadcast=True)

@socketio.on("handle-order")
def handle_order(order):
    print("Evento: handle-order")
    if(menu_controller.check_order(order)):
        #print("Antes de emit menu", menu_controller.menu)
        #print("Antes de emit menu solo items", menu_controller.menu['items'])
        new_order = order_controller.add_order(order)
        frequency_controller.add_order(order)
        #emit('get-complete-menu',menu_controller.get_complete_menu() , broadcast=True)
        emit('get-complete-menu', menu_controller.menu , broadcast=True)
        emit('get-summary-order', order_controller.get_summary_order(new_order), broadcast=True)
        emit('get-waiting-order', new_order, broadcast = True)
        emit('set-frequency', frequency_controller.get_list_of_frequency(), broadcast=True)
        #tambien se deberia enviar a ordenes en espera
        #este state a continuacion es de la respuesta, se deberia cambiar el state de respues para no
        #confundirlo con el state de en q cola se encuetra
        answer = {}
        answer['state'] = 1
        emit('answer-order', answer)
        print("Evento: handle-order Accept")
    else:
        answer = {}
        answer['state'] = 2
        emit('answer-order', answer)
        print("Evento: handle-order Denied")

#dashboard
@socketio.on("get-summary")
def get_summary():
    print("Evento: get-summary")
    emit('get-summary', order_controller.get_summary(), broadcast=True)

@socketio.on("set-frequency")
def set_frequency():
    print("Evento: set-frequency")
    emit('set-frequency', frequency_controller.get_list_of_frequency(), broadcast=True)
    print(frequency_controller.get_list_of_frequency())

#orders
@socketio.on("get-all-waiting-order")
def get_all_waiting_order():
    print("Evento: get-all-waiting-order")
    emit('get-all-waiting-order', order_controller.get_all_waiting_order(), broadcast=True)

@socketio.on("order-waiting-to-preparating")
def order_waiting_to_preparating(order):
    print("Evento: order-waiting-to-preparating")
    order_controller.order_waiting_to_preparating(order)

@socketio.on("get-all-preparating-order")
def get_all_preparating_order():
    print("Evento: get-all-preparating-order")
    emit('get-all-preparating-order', order_controller.get_all_preparating_order(), broadcast=True)

@socketio.on("order-preparating-to-ready")
def order_preparating_to_ready(change_order):
    print("Evento: order-preparating-to-ready")
    order = order_controller.order_preparating_to_ready(change_order)
    emit('get-ready-order', order, broadcast = True)

#finished orders
@socketio.on("get-all-ready-order")
def get_all_ready_order():
    print("Evento: get-all-ready-order")
    emit('get-all-ready-order', order_controller.get_all_ready_order(), broadcast=True)

@socketio.on("order-ready-to-commited")
def order_ready_to_commited(order):
    print("Evento: order-ready-to-commited")
    order_controller.order_ready_to_commited(order)

@socketio.on("get-all-commited-order")
def get_all_commited_order():
    print("Evento: get-all-commited-order")
    emit('get-all-commited-order', order_controller.get_all_commited_order(), broadcast=True)




'''
@socketio.on("connect")
def handle_connect():
    print("Client connected!")

#cliente
@socketio.on("send-menu")
def send_menu():
    print("Evento: send-menu")
    emit('receive-menu', menu_controller.menu, broadcast=True)














@socketio.on("get-items-from-menu")
def get_menus(id_menu):
    print("Evento: get-items-from-menu")
    emit('get-items-from-menu', menu_controller.get_all_items_from_menu(id_menu), broadcast=True)

@socketio.on("handle-menu")
def handle_menu(menu):
    print("Evento: handle-menu")
    menu_controller.set_menu(menu)
    emit('receive-menu', menu_controller.get_menu_items(), broadcast=True)

#esta funcion solo deberia
@socketio.on("send-menu")
def send_menu():
    print("Evento: send-menu")
    emit('receive-menu', menu_controller.get_menu_items(), broadcast=True)







#order

@socketio.on("get-all-order")
def get_all_order():
    emit('get-all-order', order_controller.orders_queue, broadcast=True)
    #tambien se deberia enviar a ordenes en espera
    print("Se recibio y envio todas las ordenes al orders")



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

'''



'''
#levi
@socketio.on('handleOrder')
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
'''