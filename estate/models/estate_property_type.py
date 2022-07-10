

from email.policy import default
import re
from pkg_resources import require
from odoo import fields,models,api


class estate_property(models.Model):
    _name ='estate.type'
    _description = 'estate_type'
    _order='name'
    
    # _order = 'sequence'
    name = fields.Char(default='Type Name',required=True)
    property_ids = fields.One2many('estate.property','property_type_id') 
    # trường sequence với widget = 'handel' để kéo thả sắp xếp trên tree
    sequence = fields.Integer(string='Sequence',default=1)
    # trường offer_ids realted từ model estate.type sang model estate.property.offer thông qua model estate_property (giống bắc cầu)
    # comoel_name -> tên model cần related
    # inverse_name là trường đảo ngược many2one trong model estate_property của one2many
    offer_ids = fields.One2many(comodel_name='estate.property.offer',inverse_name='property_type_id',related='property_ids.offer_ids',store=True)

    offer_count = fields.Integer(compute='_offer_count')
    _sql_constraints=[('unique_name','unique(name)','The name must be unique')]

    @api.depends('offer_ids')
    def _offer_count(self):
        for record in self:
            offer_count = self.env['estate.property.offer'].search_count([('property_type_id','=',record.id)])
            record.offer_count = offer_count
    
    def Accept(self):
        self.status = 'Accepted'
        self.property_ids.buyer_id = self.offer_ids.partner_id
        self.property_ids.selling_price = self.offer_ids.price
        self.property_ids.state = 'offer_accepted'
        
    
    def Refuse(self):
        self.status = 'Refused'

   
   