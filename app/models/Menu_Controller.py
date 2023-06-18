from .Menu import Menu
from .Menu_Item import MenuItem
class MenuController:
    def __init__(self):
        self.menu_database = Menu()
        self.menu_item_database = MenuItem()
        self.menu = {}
    def set_menu(self, id_menu):
        #print("Entre get Menu")
        all_menu = self.menu_item_database.get_all_item_from_menu(id_menu)
        for item in all_menu:
            #print("item:",item)
            self.menu[item['id_item']] = {'amount' : 0, 'name': item['_name'], 'type': item['_type'], 'description': item['_description'], 'price': item['_price'], 'image': item['_image']}

