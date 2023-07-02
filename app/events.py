from flask import request
from flask_socketio import emit

from .extensions import socketio
from .models.Menu_Controller import MenuController


menu_controller = MenuController()

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