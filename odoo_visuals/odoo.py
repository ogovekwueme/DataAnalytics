from odoorpc import ODOO

class Odoo:
    def __init__(self, host, port, db, email, password):
        self.odoo = ODOO(host, port)
        self.email = email
        self.password = password
        self.db = db
        self.login()
    def login(self):
        self.odoo.login(self.db, self.email, self.password)
        return self.odoo
    def get_user(self):
        return self.odoo.env.user
    def get_customers(self):
        return self.odoo.env['res.partner']
    def get_products(self):
        return self.odoo.env['product.product']
    def get_sale_orders(self) "
        return self.odoo.env['sale.order']
    def get_sale_order_lines(self):
        return self.odoo.env['sale.order.line']
