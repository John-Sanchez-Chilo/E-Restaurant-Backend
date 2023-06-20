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
def handle_order():
    emit('receive-menu', menu_controller.menu, broadcast=True)
    print("Se envio el menu")

#administrador
@socketio.on("get-menus")
def get_menus(obje):
    emit('get-menus', menu_controller.get_menus(), broadcast=True)
    print("Se envio los menus")

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
    print("Se envio la orden")


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