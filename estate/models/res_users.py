
from odoo import models,fields

class User(models.Model):
    _inherit ='res.users'
    _description='res'

    property_ids = fields.One2many(comodel_name='estate.property',inverse_name='salesman_id')
    

   
