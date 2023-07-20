from app.extensions import mysql_pool
class Menu:
    def __init__(self):
        self.mysql_pool = mysql_pool

    def add_menu(self, _name, _description):
        params = {
                '_name': _name,
                '_description': _description,
        }
        query = 'insert into menu(_name, _description) values ( %(_name)s, %(_description)s)'
        cursor = self.mysql_pool.execute(query, params, commit=True)
        data = {'_name': _name, '_description': _description}
        return data
    def get_menu(self, id_menu):
        params = {'id_menu' : id_menu}
        cursor = self.mysql_pool.execute('select id_menu, _name, _description from menu where id_menu=%(id_menu)s', params)
        rv = cursor[0]
        data = {'id_menu': rv[0], 'name': rv[1], 'description': rv[2]}
        return data
    def get_all_menu(self):
        cursor = self.mysql_pool.execute('select * from menu')
        data = []
        for rv in cursor:
                content = {'id_menu': rv[0], 'name': rv[1], 'description': rv[2]}
                data.append(content)
        return data
    def delete_menu(self, id_menu):
        params = {'id_menu' : id_menu}
        query = 'delete from menu where id_menu = %(id_cliente)s'
        self.mysql_pool.execute(query, params, commit=True)
        data = {'result': 1}
        return data