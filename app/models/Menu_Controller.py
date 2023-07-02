from .Menu import Menu
from .Menu_Item import MenuItem
class MenuController:
    def __init__(self):
        self.menu_database = Menu()
        self.menu_item_database = MenuItem()
        self.menu = {'items': []}
    
    def get_menus(self):
        return self.menu_database.get_all_menu() #devuelve un array de objetos menu
    
    #esta no esta siendo usada
    def get_all_items_from_menu(self, id_menu):
        return self.menu_item_database.get_all_item_from_menu(id_menu) #devuelve un array de objetos item
    
    def set_actual_menu(self, menu):
        self.menu = menu
        self.menu['items'] = self.menu_item_database.get_all_item_from_menu(menu['id_menu'])
        for item in self.menu['items']:
            item['amount'] = 0
            item['enabled'] = False
        print(self.menu)
        return 1
    
    def get_complete_menu(self):
        if(self.menu == None):
            return {'data': 0}
        return self.menu

    def enable_item(self, id_item, amount):
        print("enable", self.menu['items'])
        for item in self.menu['items']:
            if(item['id_item'] == id_item):
                item['amount'] = amount
                item['enabled'] = True
    
    def disable_item(self, id_item):
        for item in self.menu['items']:
            if(item['id_item'] == id_item):
                item['enabled'] = False
    
    #Cliente

    def get_ready_menu(self):
        ready_menu = {'items': []}
        print("items", self.menu['items'])
        for item in self.menu['items']:
            if(item['amount'] > 0 and item['enabled'] == True):
                ready_menu['items'].append(item)
        print("ready menu", ready_menu)
        return ready_menu
    
    #--------------------------------

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