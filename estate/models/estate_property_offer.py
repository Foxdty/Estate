
from asyncio.windows_events import NULL
from email.policy import default
from pickle import TRUE
from odoo import fields,models,api,tools
from odoo.exceptions import UserError
class estate_property_offer(models.Model):
    _name='estate.property.offer'
    _description='offer'
    _order = 'price desc'

    price=fields.Float(required=True,default=0)
    status = fields.Selection([('Accepted','Accepted'),('Refused','Refused')])
    partner_id = fields.Many2one('res.partner',required=True)
    validity = fields.Integer(string='Validity (days)',default=0)
    deadline = fields.Datetime(string='Deadline',default= lambda self: fields.Datetime.today())
    property_id= fields.Many2one('estate.property',required=True)
    # đối với trường có type = many2one thì k cần trường đảo ngược.
    property_type_id = fields.Many2one(comodel_name='estate.type', related='property_id.property_type_id',store=True)

    _sql_constraints=[('check_price','check(price>=0)','The price must be strictly posititive')]
    def Accept(self):
        self.status = 'Accepted'
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price
        self.property_id.state = 'offer_accepted'
        
    
    def Refuse(self):
        self.status = 'Refused'
    
    @api.model
    def create(self,vals):
        estate_property = self.env['estate.property'].browse(vals['property_id'])
        if tools.float_compare(estate_property.best_price,vals['price'],precision_digits=3)>=0:
            raise UserError("The offer must be higher than $%.2f" % estate_property.best_price)
        estate_property.state='offer_receved'
        return super().create(vals)
    