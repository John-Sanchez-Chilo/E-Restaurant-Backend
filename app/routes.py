#en caso se vaya a usar blueprints se colocaran aqui
from flask import Blueprint, jsonify, request
from .models.Menu_Item import MenuItem
from .extensions import menu_model, menu_item_model, item_model
from .models.Receipt import Receipt


bp = Blueprint('main', __name__)
receipt_model = Receipt()

@bp.route('/api/get_menus', methods=['GET'])
def get_menus():
    #esta funcion retora todos los menus
    #devuelve su nombre, descripcion, cantidad de platos
    #content = user_model.login(request.json['email'], request.json['password_'])
    #return jsonify(content)
    print("aPI get_menus")
    return jsonify(menu_model.get_all_menu())

@bp.route('/api/get_items_from_menu', methods=['POST'])
def get_items_from_menu(id_menu):
    #devuelve la informacion de los platos de un menú en específico.
    return menu_item_model.get_all_item_from_menu(id_menu)

@bp.route('/api/get_items', methods=['GET'])
def get_items():
    #esta funcion retora todos los items
    return jsonify(item_model.get_all_item())

@bp.route('/api/create_menu', methods=['POST'])
def create_menu():
    content = request.get_json()
    print(content)
    menu_model.add_menu(content['name'], content['description'], content['n_items'])
    menu = menu_model.get_menu_by_name(content['name'])
    for id_item in content['items']:
        menu_item_model.add_menu_item(menu['id_menu'], id_item)
    #return jsonify(item_model.get_all_item())
    print("created menu and items")
    return {'status': 1}

@bp.route('/api/delete_menu', methods=['POST'])
def delete_menu():
    content = request.get_json()
    print(content)
    menu_model.delete_menu(int(content['id_menu']))
    return {'status': 1}

@bp.route('/api/get_receipt', methods=['POST'])
def get_receipts():
    #funcion para obtener los bills en funcion de parametros como monto total, y fecha
    return receipt_model.get_all_receipt()