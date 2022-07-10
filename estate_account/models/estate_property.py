
from os import access
from odoo import models

class EstateProperty(models.Model):
    _inherit ="estate.property"

    def Sold(self):

        self.check_access_rights('unlink')
        self.check_access_rule('unlink')
        journal = self.env['account.move'].sudo().with_context(default_move_type='out_invoice')._get_default_journal()
        print('journal--------------------->',journal)
        self.env['account.move'].sudo().create({
            'partner_id':self.buyer_id,
            'move_type':'out_invoice',
            'journal_id': journal.id,
            'invoice_line_ids': [
                    ({
                        'name':'Available house',
                        'quantity': 1,
                        'price_unit':self.selling_price*0.06 + self.selling_price
                    }),
                    ({
                        'name':'Administrative fees',
                        'quantity':1,
                        'price_unit':100.00
                    })
                ]
        })
        print('Đã tạo ')
        return super().Sold()
    
    
    
    


    