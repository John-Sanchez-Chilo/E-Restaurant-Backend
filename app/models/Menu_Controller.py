from .Menu import Menu
from .Menu_Item import MenuItem
class MenuController:
    def __init__(self):
        self.menu_database = Menu()
        self.menu_item_database = MenuItem()
        self.menu = {
            'name' : "Fin de semana",
            'description': "Menu de fin de semana"
        }
    
    def get_menus(self):
        return self.menu_database.get_all_menu()
    
    def get_all_items_from_menu(self, id_menu):

        return self.menu_item_database.get_all_item_from_menu(id_menu)

    def set_menu(self, menu):
        self.menu['items'] = menu

    def set_current_menu(self, id_menu):
        #print("Entre get Menu")
        all_menu = self.menu_item_database.get_all_item_from_menu(id_menu)
        for item in all_menu:
            #print("item:",item)
            self.menu[item['id_item']] = {'amount' : 0, 'name': item['_name'], 'type': item['_type'], 'description': item['_description'], 'price': item['_price'], 'image': item['_image']}

    def get_menu_items(self):
        return self.menu