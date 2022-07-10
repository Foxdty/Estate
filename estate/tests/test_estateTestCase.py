
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged

@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        test_name_1=cls.env['estate.property'].create({'name':123})
        test_name_2=cls.env['estate.property'].create({'name':123})
        cls.assertEqual(test_name_1.usage,test_name_2.usage)
        print('Test is successfull')
        return super().setUpClass()
