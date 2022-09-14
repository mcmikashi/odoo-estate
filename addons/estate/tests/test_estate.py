from odoo.tests.common import TransactionCase
from odoo.tests import tagged
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import Form


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
            'expected_price':150000,
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

        cls.property_vals_1 = {
            'name':'The Coach House 1',
            'expected_price':5000000,
        }
        cls.properties_1 = cls.env['estate.property'].create([cls.property_vals_1])

        cls.property_vals_2 = {
            'name':'The Coach House 2',
            'expected_price':5000000,
            'state':'canceled',
        }
        cls.properties_2 = cls.env['estate.property'].create([cls.property_vals_2])
    
        cls.property_vals_3 = {
            'name':'The Coach House 3',
            'expected_price':5000000,
            'state':'sold',
        }
        cls.properties_3 = cls.env['estate.property'].create([cls.property_vals_3])

        cls.offer_vals_0 = {
            "property_id":cls.properties_0.id,
            "price":150000,
            "partner_id":cls.buyer.id,
        }
        cls.estate_offer_0 = cls.env['estate.property.offer'].create(cls.offer_vals_0)

        cls.offer_vals_1 = {
            "property_id":cls.properties_0.id,
            "price":195000,
            "partner_id":cls.buyer.id,
        }
        cls.estate_offer_1 = cls.env['estate.property.offer'].create(cls.offer_vals_1)

        cls.offer_vals_2 = {
            "property_id":cls.properties_0.id,
            "price":50000,
            "partner_id":cls.buyer.id,
            }
        cls.estate_offer_2 = cls.env['estate.property.offer'].create(cls.offer_vals_2 )
    
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
            'best_offer_price':self.offer_vals_1["price"]
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

    def test_action_sell_properties(self):
        # test a property with acepted offer and default state
        self.estate_offer_0.state = 'accepted'
        self.properties_0.action_sell()
        self.assertRecordValues(self.properties_0,[{'state':'sold'}])

        with self.assertRaises(UserError):
            # test action sell with no accepted offer for the proterty
            self.properties_1.action_sell()
        
        with self.assertRaises(UserError):
            # test action sell the proterty what is cancel
            self.properties_2.action_sell()
    
    def test_action_cancel_properties(self):
        # test a property that have a default state
        self.properties_0.action_cancel()
        self.assertRecordValues(self.properties_0,[{'state':'canceled'}])
        with self.assertRaises(UserError):
            # test action cancel with solded property
            self.properties_3.action_cancel()

    def test_action_accept_offer(self):
        with self.assertRaises(ValidationError):
            self.assertFalse(self.estate_offer_2.state)
            self.estate_offer_2.action_accept_offer()
        self.assertFalse(self.estate_offer_1.state)
        self.estate_offer_1.action_accept_offer()
        self.assertRecordValues(self.estate_offer_1,[{'state':'accepted'}])
        self.assertRecordValues(self.properties_0,[
            {'selling_price':self.offer_vals_1["price"],
             'buyer_id':self.offer_vals_1["partner_id"],
             'state':'offer accepted'}])
        with self.assertRaises(UserError):
            # test action when an offer is already accepted
            self.estate_offer_0.action_accept_offer()

    def test_action_refuse_offer(self):
        self.assertFalse(self.estate_offer_1.state)
        self.estate_offer_1.action_refuse_offer()
        self.assertRecordValues(self.estate_offer_1,[{'state':'refused'}])

    def test_form_property(self):
        """Test the onchange function of the estate property form"""
        with Form(self.properties_1) as prop:
            self.assertEqual(prop.garden_area, 0)
            self.assertFalse(prop.garden_orientation)
            prop.garden = True
            self.assertEqual(prop.garden_area, 10)
            self.assertEqual(prop.garden_orientation, "north")
            prop.garden = False
            self.assertEqual(prop.garden_area, 0)
            self.assertFalse(prop.garden_orientation)
