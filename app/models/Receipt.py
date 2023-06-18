from extensions import mysql_pool
class Receipt:
    def __init__(self):
        self.mysql_pool = mysql_pool

    def add_receipt(self, date_time, _total_amount):
        params = {
                'date_time': date_time,
                '_total_amount': _total_amount,
        }
        query = 'insert into receipt(date_time, _total_amount) values ( %(date_time)s, %(_total_amount)s)'   
        cursor = self.mysql_pool.execute(query, params, commit=True)
        data = {'date_time': date_time, '_total_amount': _total_amount}
        return data
    def get_receipt(self, id_receipt):
        params = {'id_receipt' : id_receipt}
        cursor = self.mysql_pool.execute('select id_receipt, date_time, _total_amount from receipt where id_receipt=%(id_receipt)s', params)
        rv = cursor[0]
        data = {'id_receipt': rv[0], 'date_time': rv[1], '_total_amount': rv[2]}
        return data
    def get_all_receipt(self):
        cursor = self.mysql_pool.execute('select * from receipt')
        data = []
        for rv in cursor:
                content = {'id_receipt': rv[0], 'date_time': rv[1], '_total_amount': rv[2]}
                data.append(content)
        return data
    def delete_receipt(self, id_receipt):
        params = {'id_receipt' : id_receipt}
        query = 'delete from receipt where id_receipt = %(id_cliente)s'
        self.mysql_pool.execute(query, params, commit=True)
        data = {'result': 1}
        return data