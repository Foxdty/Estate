from email.policy import default
from modulefinder import Module

from pkg_resources import require
from odoo import fields,models
class estate_property_tag(models.Model):
    _name='estate.tag'
    _description='estate_property_tag'
    _order='name'

    name=fields.Char(string='Name',default='Tag',required=True)
    color = fields.Integer(string='Color',default=1)