# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Real Estate',
    'version': '1.2',
    'category': 'Sales/Estate',
    'sequence': 1,
    'summary': ' opportunities',
    'description': "",
    'license': 'OEEL-1',
    'website': '',
    'depends': [
        'base',
        'mail',
        'web',
        'board'
        
       
        

        
   
        
    ],
    
    'data': [
        'security/ir.model.access.csv' ,
        'security/security.xml',
        'security/res_company.xml',
        'views/estate_property_views.xml' ,
        'views/property_type_view.xml' ,
        'views/estate_menus.xml' ,
        'views/estate_tag.xml',
        'views/res_users_view.xml',
        
        'report/estate_detail_template.xml', 
        'report/estate_property_report.xml',
        'report/reprot.xml',
        
          
        
    ],
    "demo": [
        "demo/demo_data.xml"
    ],
    'installable': True,
    'application': True,
    'auto_install': True
}