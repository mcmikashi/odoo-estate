from odoo.tests.common import TransactionCase
#from odoo.exceptions import UserError
from odoo.tests import tagged
from datetime import date
from dateutil.relativedelta import relativedelta


# The CI will run these tests after all the modules are installed,
# not right after installing the one defining it.
@tagged('standard', 'at_install','post_install')
class EstateTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        # add env on cls and many other things
        super(EstateTestCase, cls).setUpClass()

        # create the data for each tests. By doing it in the setUpClass instead
        # of in a setUp or in each test case, we reduce the testing time and
        # the duplication of code.
        cls.vals_tags_0 = {'name':'cozy'}
        cls.properties_tags_0 = cls.env['estate.property.tags'].create([cls.vals_tags_0])

        cls.vals_type_0 = {'name':'villa'}
        cls.properties_type_0 = cls.env['estate.property.type'].create([cls.vals_type_0])
        
        cls.vals_buyer = {'name': 'Dupont Dupont'}
        cls.buyer = cls.env['res.partner'].create(cls.vals_buyer)

        cls.property_vals_0 = {
            'name':'The Coach House',
            'description': 'A house that is situated above a row of garages or carports.',
            'postcode': '97300',
            'expected_price':1500000,
            'selling_price' :1800000,
            'living_area' :250,
            'facades' : 6,
            'garage' :True,
            'garden' :True,
            'garden_area' : 500,
            'garden_orientation' : 'north',
            'property_type_id':cls.properties_type_0.id,
            'tag_ids': [cls.properties_tags_0.id],
        }
        cls.properties_0 = cls.env['estate.property'].create([cls.property_vals_0])

        cls.offer_vals_0 = {
            "property_id":cls.properties_0.id,
            "price":1800000,
            "partner_id":cls.buyer.id,
            "status":'accepted',
        }
        cls.estate_offer_0 = cls.env['estate.property.offer'].create(cls.offer_vals_0)

    def test_default_date_availability(self):
        """Test that the method class _default_date_availability return the good value"""
        self.assertEqual(
            self.properties_0._default_date_availability(),
            date.today() + relativedelta(months=3)
        )

    def test_add_properties_tags(self):
        """Test that the properties tags are correctly created."""
        self.assertRecordValues(self.properties_tags_0,[self.vals_tags_0])

    def test_add_properties_type(self):
        """Test that the properties type are correctly created."""
        self.assertRecordValues(self.properties_type_0,[self.vals_type_0])

    def test_add_properties(self):
        """Test that the properties are correctly created."""
        default_date_availability = date.today() + relativedelta(months=3)
        default_values = {'bedrooms':2, 'date_availability':default_date_availability,'active':True,'state':'new'}
        computed_values = {
            'total_area': self.property_vals_0['living_area'] + self.property_vals_0['garden_area'],
            'best_offer_price':self.offer_vals_0["price"]
        }
        self.assertRecordValues(self.properties_0,[
            {**self.property_vals_0, **default_values, **computed_values}
        ])
    
    def test_add_properties_offers(self):
        """Test that the properties tags are correctly created."""
        default_date_dead_line = date.today() + relativedelta(days=7)
        default_values = {'validity':7}
        computed_values = {'date_deadline':default_date_dead_line}
        self.assertRecordValues(self.estate_offer_0,[
            {**self.offer_vals_0, **default_values, **computed_values}
        ])
