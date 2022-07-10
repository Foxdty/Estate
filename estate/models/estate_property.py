
from odoo import fields,models,api
from odoo.exceptions import UserError, ValidationError


class estate_property(models.Model):
    _name ='estate.property'
    _inherit=['mail.thread','mail.activity.mixin']
    _description = 'My Estate'
    _order = 'id desc'
    
    # _order = 'sequence'
    name = fields.Char(default='Estate Name')
    last_seen = fields.Datetime("Last seen", default=lambda self: fields.Datetime().now())
    bedrooms = fields.Integer(default=2)
    active = fields.Boolean("Active", default=True)
    postcode = fields.Integer(string='Postcode')
    expected_price = fields.Float(string='Expected Price',default=0)
    facades = fields.Integer(string='Facades',default=0)
    garden = fields.Boolean('Garden',default=False)
    garden_orientation = fields.Selection([('1','North'),('2','East'),('3','South'),('4','West')])
    selling_price = fields.Float(string='Selling price',default=0.00)
    living_area = fields.Integer(string='Living Area (sqm)',default=0)
    garage = fields.Boolean(string='Garage',default=False)
    garden_area = fields.Integer(string='Garden Area (sqm)',default=0)
    adress = fields.Text(string="Adress")
    availability_date = fields.Datetime("Availability From",default=lambda self: fields.Datetime.today())
    description = fields.Text(string="Desciption")
    status = fields.Char(string='Status',default='New')
    state = fields.Selection([('new','New'),('offer_receved','OFFER RECEVED'),
    ('offer_accepted','OFFER ACCEPTED'),('sold','SOLD')],default='new',string='State',required=True)
    # Lấy tên nhân viên hệ thống (tên nhân viên bán hàng)
    salesman_id = fields.Many2one('res.users',string='Salesman',default=lambda self: self.env.user)
    # Lấy tên người mua (người mua có thể là doanh nghiệp, cửa hàng, cá nhân...)
    buyer_id = fields.Many2one('res.partner',string="Buyer")
    # Trường many2many để chỉ tới model estate_property_tag
    tag_ids = fields.Many2many('estate.tag',string='TAG')

    # Trường offer_ids sử sụng type = one2many để tham chiếu tới model estate.property.offer và là 
    # trường đảo ngược của many2one (tức là bên model estate.property.offer có một trường tên property_id  sử dụng type = many2one)
    offer_ids=fields.One2many('estate.property.offer','property_id',string='Offer')
    # Trường property_type_id có type = many2one để tham chiếu tới model estate.type
    property_type_id=fields.Many2one(comodel_name='estate.type')
    ###
    user_id = fields.Many2one('res.users',string='user')

    total_area = fields.Float(compute='_total_area')

    best_price = fields.Float(compute='_best_price')
    # Bảo mật đa công ty
    company_id=fields.Many2one('res.company',required=True,default= lambda self: self.env.user.company_id)
    # Đặt điều kiện cho các fields như trường expected_price >0 
    # Trường name phải khác tên nhau
    #Trường selling_price >=0
    _sql_constraints = [('check_expected_price','check(expected_price > 0 )','The expected price must be strictly posititive'),
    
    ('check_selling_price','check(selling_price>=0)','The selling price must be strictly posititive')
    ]
    #('unique_name','unique(name)','The name must be unique'),
    # @api.depends để tính toán 
    @api.depends('living_area','garden_area')
    def _total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('offer_ids.price')
    def _best_price(self):
        
        for record in self:
            try:
                record.best_price = max(record.mapped('offer_ids.price'))
            except ValueError:
                record.best_price = record.offer_ids.price = 0
    # @api.onchange để check sự thay đổi như trường garden có sự thay đổi giữa true or false.
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = '1'
            print('change')
        else:
            self.garden_area = 0
            self.garden_orientation = None
            print('change false')
    def Sold(self):
        if self.status == 'Canceled':
            raise UserError('Canceled properties cannot be sold')
        else:
            self.status = 'Sold'
            if self.state == 'offer_accepted':
                self.state = 'sold'
                print('Estate: -->>>>>>>>>>')
            
        

    def Cancel(self):
        if self.status == 'Sold':
            raise UserError('Sold properties cannot be Cancel')
        else:
            self.status = 'Canceled'

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price != 0.00:
                x = record.expected_price * 0.9
           
                if record.selling_price < x:
                    raise ValidationError('Selling price have not to much smaller than expected price')
        

    def unlink(self):
        if self.status != 'Sold':
            return super(estate_property,self).unlink()
        else:
            raise UserError('Only New and Canceled properties can be delete')
    

    

