# $Id: declarations.template,v 1.2 2000/04/13 02:08:56 davis Exp davis $
# Copyright (C) 1999 LinuXden, All Rights Reserved
# Copright Statement at http://www.linuxden.com/copyrighted_apps.html
# 
# it is imperative that there is white space between the = in following lines
store_info = {}
store_info['db_name'] = 'fsbowv'
store_info['domain_name'] = 'www.fsbowv.com'
store_info['browser_username'] = 'userfsbo'
store_info['browser_password'] = 'fsbo'
store_info['help_file'] = 'test.html'

def table_privileges():
    privileges = { \
	'store_info' : { \
	    store_info['browser_username'] : ['SELECT','INSERT','UPDATE'] \
	    }, \
	'customers' : { \
	    store_info['browser_username'] : ['SELECT','INSERT','UPDATE'] \
	    }, \
	'orders' : { \
	    store_info['browser_username'] : ['SELECT','INSERT'] \
	    },
	'order_items' : { \
	    store_info['browser_username'] : ['SELECT','INSERT','UPDATE'] \
	    },
	'sales_tax_by_state' : { \
	    store_info['browser_username'] : ['SELECT'] \
	    },
	'product_categories' : { \
	    store_info['browser_username'] : ['SELECT'] \
	    },
	'payment_methods' : { \
	    store_info['browser_username'] : ['SELECT'] \
	    },
	'order_status_values' : { \
	    store_info['browser_username'] : ['SELECT'] \
	    },
	'market_status_values' : { \
	    store_info['browser_username'] : ['SELECT'] \
	    },
	'shipping_methods' : { \
	    store_info['browser_username'] : ['SELECT'] \
	    },
	'products' : { \
	    store_info['browser_username'] : ['SELECT'] \
	    },
	'properties' : { \
	    store_info['browser_username'] : ['SELECT','INSERT','UPDATE'] \
	    }, \
	'internet_ad_items' : { \
	    store_info['browser_username'] : ['SELECT'] \
	    }, \
	'properties_id_seq' : { \
	    store_info['browser_username'] : ['SELECT','INSERT','UPDATE'] \
	    }, \
	'customer_id_seq' : { \
	    store_info['browser_username'] : ['SELECT','INSERT','UPDATE'] \
	    }, \
	'orders_id_seq' : { \
	    store_info['browser_username'] : ['SELECT','INSERT','UPDATE'] \
	    }, \
	'products_id_seq' : { \
	    store_info['browser_username'] : ['SELECT'] \
	    } \
	}

    return privileges

def define_tables():
    data_tables = { \
	'store_info' : { \
	    'id' : { \
		'label' : 'Store Id', \
		'type': 'VARCHAR', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : '1', \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
		'leaveFocus' : "checkBlankField(this, 'Id')", \
		'gainFocus' : "displayHint('Enter your store id')" \
		}, \
	    'name': { \
		'label' : 'Name', \
		'type' : 'VARCHAR', \
		'db_size' : '30', \
		'form_size' : '30', \
		'default' : 'None', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 2, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.name',"'Name'"], \
		'leaveFocus' : "checkBlankField(this, 'Name')", \
		'gainFocus' : "displayHint('Enter your Store Name')" \
		}, \
	    'address_line_1': { \
		'label' : 'Address Line 1', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : 'None', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 3, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.address_line_1',"'Store Address Line 1'"], \
		'leaveFocus' : "checkBlankField(this, 'Store Address Line 1')", \
		'gainFocus' : "displayHint('Enter your Store Address Line 1')" \
		}, \
	    'address_line_2': { \
		'label' : 'Address Line 2', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : 'None', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 4, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter your Store Address Line 2')" \
		}, \
	    'city' : { \
		'label' : 'City (Billing)', \
		'type' : 'VARCHAR', \
		'db_size' : '60', \
		'form_size' : '60', \
		'default' : 'None', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 5, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.city',"'City'"], \
		'leaveFocus' : "checkBlankField(this, 'City')", \
		'gainFocus' : "displayHint('Enter the city')" \
		}, \
	    'state' : { \
		'label' : 'State (Billing)', \
		'type' : 'VARCHAR', \
		'db_size' : '2', \
		'form_size' : '2', \
		'default' : 'NA', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 6, \
		'required' : 1, \
		'leaveFocus' : "checkBlankField(this, 'State')", \
		'gainFocus' : "displayHint('Enter the abbreviated state')", \
		'lov' : "SELECT state_abbreviation FROM sales_tax_by_state ORDER BY state_abbreviation" \
		}, \
	    'zip' : { \
		'label' : 'Zip Code', \
		'type' : 'VARCHAR', \
		'db_size' : '5', \
		'form_size' : '5', \
		'default' : 'None', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 7, \
		'required' : 1, \
		'validation_routine' : 'valid_integer', \
		'validation_arguments' : ['form.zip',"''","'Zip Code (Billing)'","true"], \
		'leaveFocus' : "checkBlankField(this, 'Zip Code')", \
		'gainFocus' : "displayHint('Enter the zip code')" \
		}, \
	    'owner': { \
		'label' : 'Owner Name', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : 'None', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 8, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.owner',"'Owner Name'"], \
		'leaveFocus' : "checkBlankField(this, 'Owner Name')", \
		'gainFocus' : "displayHint('Enter Store Owner Name')" \
		}, \
	    'email' : { \
		'label' : 'E-mail Address', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : 'None', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 9, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the store e-mail address')" \
		}, \
	    'phone_number_voice' : { \
		'label' : 'Phone Number (Voice)', \
		'type' : 'VARCHAR', \
		'db_size' : '12', \
		'form_size' : '12', \
		'default' : 'None', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 10, \
		'validation_routine' : 'valid_format', \
		'validation_arguments' : ["form.phone_number_voice","'###-###-####'","'Daytime Phone Number'","false"], \
		'leaveFocus' : "checkBlankField(this, 'Phone Number (Voice)')", \
		'gainFocus' : "displayHint('Enter the phone number (Voice)')", \
		'format' : "###-###-####" \
		}, \
	    'phone_number_fax' : { \
		'label' : 'Phone Number (FAX)', \
		'type' : 'VARCHAR', \
		'db_size' : '12', \
		'form_size' : '12', \
		'default' : 'None', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 11, \
		'validation_routine' : 'valid_format', \
		'validation_arguments' : ["form.phone_number_fax","'###-###-####'","'Daytime Phone Number'","false"], \
		'leaveFocus' : "checkBlankField(this, 'Phone Number (FAX)')", \
		'gainFocus' : "displayHint('Enter the phone number (FAX)')", \
		'format' : "###-###-####" \
		}}, \
	'customers' : { \
	    'id' : { \
		'label' : 'Customer Id', \
		'type': 'VARCHAR', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
		'leaveFocus' : "checkBlankField(this, 'Id')", \
		'gainFocus' : "displayHint('Enter your customer id')" \
		}, \
	    'first_name' : { \
		'label' : 'First Name', \
		'type' : 'VARCHAR', \
		'db_size' : '50', \
		'form_size' : '50', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 2, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.first_name',"'First Name'"], \
		'leaveFocus' : "checkBlankField(this, 'First Name')", \
		'gainFocus' : "displayHint('Enter your First Name')" \
		}, \
	    'middle_initial' : { \
		'label' : 'Middle Initial', \
		'type' : 'VARCHAR', \
		'db_size' : '1', \
		'form_size' : '1', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 3, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter your Middle Initial')" \
		}, \
	    'last_name' : { \
		'label' : 'Last Name', \
		'type' : 'VARCHAR', \
		'db_size' : '50', \
		'form_size' : '50', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 4, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.last_name',"'Last Name'"], \
		'leaveFocus' : "checkBlankField(this, 'Last Name')", \
		'gainFocus' : "displayHint('Enter your Last Name')" \
		}, \
	    'street_1' : { \
		'label' : 'Street Line 1 (Billing)', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 5, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.street_1',"'Street Line 1 (Billing)'"], \
		'leaveFocus' : "checkBlankField(this, 'Street Line 1 (Billing)')", \
		'gainFocus' : "displayHint('Enter your address')" \
		}, \
	    'street_2' : { \
		'label' : 'Street Line 2 (Billing)', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 6, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter your street address')" \
		}, \
	    'city' : { \
		'label' : 'City (Billing)', \
		'type' : 'VARCHAR', \
		'db_size' : '60', \
		'form_size' : '60', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 7, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.city',"'City'"], \
		'leaveFocus' : "checkBlankField(this, 'City')", \
		'gainFocus' : "displayHint('Enter the city')" \
		}, \
	    'state' : { \
		'label' : 'State (Billing)', \
		'type' : 'VARCHAR', \
		'db_size' : '2', \
		'form_size' : '2', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 8, \
		'required' : 1, \
		'leaveFocus' : "checkBlankField(this, 'State')", \
		'gainFocus' : "displayHint('Enter the abbreviated state')", \
		'lov' : "SELECT state_abbreviation FROM sales_tax_by_state ORDER BY state_abbreviation" \
		}, \
	    'zip' : { \
		'label' : 'Zip Code (Billing)', \
		'type' : 'VARCHAR', \
		'db_size' : '5', \
		'form_size' : '5', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 9, \
		'required' : 1, \
		'validation_routine' : 'valid_integer', \
		'validation_arguments' : ['form.zip',"''","'Zip Code (Billing)'","true"], \
		'leaveFocus' : "checkBlankField(this, 'Zip Code')", \
		'gainFocus' : "displayHint('Enter the zip code')" \
		}, \
	    'email' : { \
		'label' : 'E-mail Address', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 10, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the e-mail address')" \
		}, \
	    'daytime_phone_number' : { \
		'label' : 'Daytime Phone Number', \
		'type' : 'VARCHAR', \
		'db_size' : '12', \
		'form_size' : '12', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 11, \
		'required' : 1, \
		'validation_routine' : 'valid_format', \
		'validation_arguments' : ["form.daytime_phone_number","'###-###-####'","'Daytime Phone Number'","true"], \
		'leaveFocus' : "checkBlankField(this, 'Daytime Phone Number')", \
		'gainFocus' : "displayHint('Enter the daytime phone number')", \
		'format' : "###-###-####" \
		}, \
	    'evening_phone_number' : { \
		'label' : 'Evening Phone Number', \
		'type' : 'VARCHAR', \
		'db_size' : '12', \
		'form_size' : '12', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 12, \
		'required' : 1, \
		'validation_routine' : 'valid_format', \
		'validation_arguments' : ["form.evening_phone_number","'###-###-####'","'Evening Phone Number'","false"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the evening phone number')", \
		'format' : "###-###-####" \
		}, \
	    'account_username' : { \
		'label' : 'Account Username', \
		'type' : 'VARCHAR', \
		'db_size' : '9', \
		'form_size' : '9', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 13, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.account_username',"'Account Username'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter a username to access your account data')" \
		}, \
	    'account_password' : { \
		'label' : 'Account Password', \
		'type' : 'VARCHAR', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'form_input_type' : 'password', \
		'value' : '', \
		'display_order' : 14, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.account_password',"'Account Password'"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter a password to access your account data')" \
		}}, \
	'orders' : { \
	    'id' : { \
		'label' : 'Order Id', \
		'type' : 'VARCHAR', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
		'leaveFocus' : "checkBlankField(this, 'Order Id')", \
		'gainFocus' : "displayHint('Enter the order id')" \
		}, \
	    'customer_id' : { \
		'label' : 'Customer Id', \
		'type' : 'VARCHAR', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 2, \
		'required' : 1, \
 		'validation_routine' : 'valid_integer', \
		'validation_arguments' : ['form.customer_id',"''","'Customer Id'","true"], \
		'leaveFocus' : "checkBlankField(this, 'Customer Id')", \
		'gainFocus' : "displayHint('Enter the customer id')" \
		}, \
	    'creation_date' : { \
		'label' : 'Creation Date', \
		'type' : 'DATE', \
		'db_size' : '4', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 3, \
		'required' : 1, \
		'validation_routine' : 'valid_date', \
		'validation_arguments' : ['form.creation_date',"'Creation Date'","true"], \
		'leaveFocus' : "checkBlankField(this, 'Order Creation Date')", \
		'gainFocus' : "displayHint('Enter the order creation date')", \
		'format' : "MM-DD-YYYY" \
		}, \
	    'shipped_date' : { \
		'label' : 'Order Ship Date', \
		'type' : 'DATE', \
		'db_size' : '4', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 4, \
		'validation_routine' : 'valid_date', \
		'validation_arguments' : ['form.shipped_date',"'Order Ship Date'","false"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the shipped date')", \
		'format' : "MM-DD-YYYY" \
		}, \
	    'processor' : { \
		'label' : 'Order Processor', \
		'type' : 'VARCHAR', \
		'db_size' : '20', \
		'form_size' : '20', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 5, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the id of the processor')" \
		}, \
	    'shipping_street1' : { \
		'label' : 'Street Line 1 (Shipping)', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 6, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.shipping_street1',"'Street Line 1 (Shipping)'"], \
		'leaveFocus' : "checkBlankField(this, 'Shipping Street Line 1')", \
		'gainFocus' : "displayHint('Enter the shipping street line 1')" \
		}, \
	    'shipping_street2' : { \
		'label' : 'Street Line 2 (Shipping)', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 7, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the shipping street line 2')" \
		}, \
	    'city' : { \
		'label' : 'City (Shipping)', \
		'type' : 'VARCHAR', \
		'db_size' : '60', \
		'form_size' : '60', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 8, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.city',"'City (Shipping)'"], \
		'leaveFocus' : "checkBlankField(this, 'City')", \
		'gainFocus' : "displayHint('Enter the city')" \
		}, \
	    'state' : { \
		'label' : 'State (Shipping)', \
		'type' : 'VARCHAR', \
		'db_size' : '2', \
		'form_size' : '2', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 9, \
		'required' : 1, \
		'leaveFocus' : "checkBlankField(this, 'State')", \
		'gainFocus' : "displayHint('Enter an abbreviated state')", \
		'lov' : "SELECT state_abbreviation FROM sales_tax_by_state ORDER BY state_abbreviation" \
		}, \
	    'zip' : { \
		'label' : 'Zip Code (Shipping)', \
		'type' : 'VARCHAR', \
		'db_size' : '5', \
		'form_size' : '5', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 10, \
		'required' : 1, \
		'validation_routine' : 'valid_integer', \
		'validation_arguments' : ['form.zip',"''","'Zip Code (Shipping)'","true"], \
		'leaveFocus' : "checkBlankField(this, 'Zip Code')", \
		'gainFocus' : "displayHint('Enter the zip code')" \
		}, \
	    'method_of_payment' : { \
		'label' : 'Payment Method', \
		'type' : 'VARCHAR', \
		'db_size' : '25', \
		'form_size' : '25', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 11, \
		'required' : 1, \
		'leaveFocus' : "checkBlankField(this, 'Payment Method')", \
		'gainFocus' : "displayHint('Enter the payment method')", \
		'lov' : "SELECT payment_type FROM payment_methods ORDER BY payment_type" \
		}, \
	    'credit_card_number' : { \
		'label' : 'Credit Card Number', \
		'type' : 'VARCHAR', \
		'db_size' : '16', \
		'form_size' : '16', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 12, \
		'required' : 1, \
		'validation_routine' : 'valid_integer', \
		'validation_arguments' : ['form.credit_card_number',"''","'Credit Card Number'","true"], \
		'leaveFocus' : "checkBlankField(this, 'Credit Card Number')", \
		'gainFocus' : "displayHint('Enter the credit card number')", \
		'format' : "################" \
		}, \
	    'card_expiration_date' : { \
		'label' : 'Credit Card Expiration Date', \
		'type' : 'DATE', \
		'db_size' : '4', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'required' : 1, \
		'display_order' : 13, \
		'validation_routine' : 'valid_date', \
		'validation_arguments' : ['form.card_expiration_date',"'Credit Card Expiration Date'","true"], \
		'leaveFocus' : "checkBlankField(this, 'Credit Card Expiration Date')", \
		'gainFocus' : "displayHint('Enter the credit card expiration date')", \
		'format' : "MM-DD-YYYY" \
		}, \
	    'shipping_method' : { \
		'label' : 'Shipping Method', \
		'type' : 'VARCHAR', \
		'db_size' : '30', \
		'form_size' : '30', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 14, \
		'required' : 1, \
		'leaveFocus' : "checkBlankField(this, 'Shipping Method')", \
		'gainFocus' : "displayHint('Enter the shipping method')", \
		'lov' : "SELECT method FROM shipping_methods ORDER BY method" \
		}, \
	    'shipping_handling' : { \
		'label' : 'Shipping Handling', \
		'type' : 'DECIMAL', \
		'db_size' : '9,2', \
		'form_size' : '10', \
		'default' : '0.00', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 15, \
		'required' : 1, \
 		'validation_routine' : 'valid_money', \
		'validation_arguments' : ['form.shipping_handling',"''","'Shipping Handling'","true"], \
		'leaveFocus' : "checkBlankField(this, 'Shipping/Handling')", \
		'gainFocus' : "displayHint('Enter the shipping/handling')" \
		}, \
	    'subtotal' : { \
		'label' : 'Subtotal', \
		'type' : 'DECIMAL', \
		'db_size' : '9,2', \
		'form_size' : '10', \
		'default' : '0.00', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 16, \
		'required' : 1, \
 		'validation_routine' : 'valid_money', \
		'validation_arguments' : ['form.subtotal',"''","'Subtotal'","true"], \
		'leaveFocus' : "checkBlankField(this, 'Subtotal')", \
		'gainFocus' : "displayHint('Enter the subtotal')", \
		'format' : "#######.##" \
		}, \
	    'sales_tax' : { \
		'label' : 'Sales Tax', \
		'type' : 'DECIMAL', \
		'db_size' : '9,2', \
		'form_size' : '10', \
		'default' : '0.00', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 17, \
		'required' : 1, \
 		'validation_routine' : 'valid_money', \
		'validation_arguments' : ['form.sales_tax',"''","'Sales Tax'","true"], \
		'leaveFocus' : "checkBlankField(this, 'Sales Tax')", \
		'gainFocus' : "displayHint('Enter the sales tax')", \
		'format' : "#######.##" \
		}, \
	    'total' : { \
		'label' : 'Total', \
		'type' : 'DECIMAL', \
		'db_size' : '9,2', \
		'form_size' : '10', \
		'default' : '0.00', \
		'display' : 'editable', \
		'value' : '', \
		'required' : 1, \
 		'validation_routine' : 'valid_money', \
		'validation_arguments' : ['form.total',"''","'Total'","true"], \
		'display_order' : 18, \
		'leaveFocus' : "checkBlankField(this, 'Total')", \
		'gainFocus' : "displayHint('Enter the total')", \
		'format' : "#######.##" \
		}, \
	    'order_status' : { \
		'label' : 'Order Status', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 19, \
		'required' : 1, \
		'leaveFocus' : "checkBlankField(this, 'Order Status')", \
		'gainFocus' : "displayHint('Enter the order status')", \
		'lov' : "SELECT status_of_order FROM order_status_values ORDER BY status_of_order" \
		}, \
	    'tracking_number' : { \
		'label' : 'Tracking Number', \
		'type' : 'VARCHAR', \
		'db_size' : '20', \
		'form_size' : '20', \
		'default' : None, \
		'display' : 'editable', \
 		'validation_routine' : 'valid_integer', \
		'validation_arguments' : ['form.tracking_number',"''","'Tracking Number'","false"], \
		'value' : '', \
		'display_order' : 20, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the tracking number')", \
		'format' : "####################" \
		}},\
	'order_items' : { \
	    'line_item' : { \
		'label' : 'Line Item', \
		'type' : 'VARCHAR', \
		'db_size' : '10', \
		'form_size' : '10',
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 1, \
		'leaveFocus' : "checkBlankField(this, 'Line Item')", \
		'gainFocus' : "displayHint('Enter the line item')" \
		}, \
	    'order_id' : { \
		'label' : 'Order Id', \
		'type' : 'VARCHAR', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 2, \
		'leaveFocus' : "checkBlankField(this, 'Order Id')", \
		'gainFocus' : "displayHint('Enter the order id')" \
		}, \
	    'product_id' : { \
		'label' : 'Product Id:', \
		'type' : 'VARCHAR', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 3, \
		'leaveFocus' : "checkBlankField(this, 'Product Id')", \
		'gainFocus' : "displayHint('Enter the product id')" \
		}, \
	    'quantity' : { \
		'label' : 'Quantity', \
		'type' : 'INT4', \
		'db_size' : '4', \
		'form_size' : '3', \
		'default' : '0', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 4, \
		'leaveFocus' : "checkBlankField(this, 'Quantity')", \
		'gainFocus' : "displayHint('Enter the quantity')", \
		'format' : "###" \
		}, \
	    'quantity_shipped' : { \
		'label' : 'Quantity Shipped', \
		'type' : 'INT4', \
		'db_size' : '4', \
		'form_size' : '3', \
		'default' : '0', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 5, \
		'leaveFocus' : "checkBlankField(this, 'Quantity Shipped')", \
		'gainFocus' : "displayHint('Enter the quantity shipped')", \
		'format' : "###" \
		}, \
	    'price' : { \
		'label' : 'Price', \
		'type' : 'DECIMAL', \
		'db_size' : '9,2', \
		'form_size' : '10', \
		'default' : '0.00', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 6, \
		'leaveFocus' : "checkBlankField(this, 'Price')", \
		'gainFocus' : "displayHint('Enter the price of product')", \
		'format' : "#######.##" \
		}, \
	    'line_subtotal' : { \
		'label' : 'Line Subtotal', \
		'type' : 'DECIMAL', \
		'db_size' : '9,2', \
		'form_size' : '10', \
		'default' : '0.00', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 7, \
		'leaveFocus' : "checkBlankField(this, 'Line Subtotal')", \
		'gainFocus' : "displayHint('Enter the line subtotal')", \
		'format' : "#######.##" \
		}}, \
	'sales_tax_by_state' : { \
	    'state_name' : { \
		'label' : 'State Full Name', \
		'type' : 'VARCHAR', \
		'db_size' : '30', \
		'form_size' : '30', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.state_name',"'State Name'"], \
		'leaveFocus' : "checkBlankField(this, 'State Full Name')", \
		'gainFocus' : "displayHint('Enter the state full name')" \
		}, \
	    'state_abbreviation' : { \
		'label' : 'State Abbreviation', \
		'type' : 'VARCHAR', \
		'db_size' : '2', \
		'form_size' : '2', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 2, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.state_abbreviation',"'State Abbreviation'"], \
		'leaveFocus' : "checkBlankField(this, 'State Abbreviation')", \
		'gainFocus' : "displayHint('Enter the state abbreviation')" \
		}, \
	    'tax' : { \
		'label' : 'Sales Tax', \
		'type' : 'DECIMAL', \
		'db_size' : '6,5', \
		'form_size' : '7', \
		'default' : '0.00', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 3, \
		'required' : 1, \
 		'validation_routine' : 'valid_money', \
		'validation_arguments' : ['form.tax',"''","'Sales Tax'","true"], \
		'leaveFocus' : "checkBlankField(this, 'Tax')", \
		'gainFocus' : "displayHint('Enter the sales tax charged in state')", \
		'format' : "#.####" \
		}}, \
	'payment_methods' : { \
	    'payment_type' : { \
		'label' : 'Payment Method', \
		'type' : 'VARCHAR', \
		'db_size' : '30', \
		'form_size' : '30', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.payment_type',"'Payment Method'"], \
		'leaveFocus' : "checkBlankField(this, 'Payment Method')", \
		'gainFocus' : "displayHint('Enter the payment method')" \
		}}, \
	'product_categories' : { \
	    'category' : { \
		'label' : 'Category', \
		'type' : 'VARCHAR', \
		'db_size' : '20', \
		'form_size' : '20', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.category',"'Category'"], \
		'leaveFocus' : "checkBlankField(this, 'Category')", \
		'gainFocus' : "displayHint('Enter a category')", \
		}}, \
	'order_status_values' : { \
	    'status_of_order' : { \
		'label' : 'Order Status', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.status_of_order',"'Order Status'"], \
		'leaveFocus' : "checkBlankField(this, 'Order Status')", \
		'gainFocus' : "displayHint('Enter the order status')" \
		}}, \
	'market_status_values' : { \
	    'status_of_market' : { \
		'label' : 'Market Status', \
		'type' : 'VARCHAR', \
		'db_size' : '25', \
		'form_size' : '25', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.status_of_market',"'Market Status'"], \
		'leaveFocus' : "checkBlankField(this, 'Market Status')", \
		'gainFocus' : "displayHint('Enter the Market status')" \
		}}, \
	'shipping_methods' : { \
	    'method' : { \
		'label' : 'Shipping Method', \
		'type' : 'VARCHAR', \
		'db_size' : '30', \
		'form_size' : '30', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 1, \
		'leaveFocus' : "checkBlankField(this, 'Shipping Method')", \
		'gainFocus' : "displayHint('Enter the shipping method')" \
		}}, \
	'products' : { \
	    'id' : { \
		'label' : 'Product Id', \
		'type' : 'VARCHAR', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
		'leaveFocus' : "checkBlankField(this, 'Id')", \
		'gainFocus' : "displayHint('Enter the product id')" \
		}, \
	    'category' : { \
		'label' : 'Category', \
		'type' : 'VARCHAR', \
		'db_size' : '20', \
		'form_size' : '20', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 2, \
		'required' : 1, \
		'leaveFocus' : "checkBlankField(this, 'Category')", \
		'gainFocus' : "displayHint('Enter a category')", \
		'lov' : "SELECT category FROM product_categories ORDER BY category" \
		}, \
	    'quantity_on_hand' : { \
		'label' : 'Quantity On Hand', \
		'type' : 'INT4', \
		'db_size' : '4', \
		'form_size' : '4', \
		'default' : '0', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 3, \
		'required' : 1, \
		'validation_routine' : 'valid_integer', \
		'validation_arguments' : ['form.quantity_on_hand',"''","'Quantity on Hand'","true"], \
		'leaveFocus' : "checkBlankField(this, 'Quantity On Hand')", \
		'gainFocus' : "displayHint('Enter the quantity on hand in inventory')", \
		'format' : "####" \
		}, \
	    'quantity_sold' : { \
		'label' : 'Quantity Sold', \
		'type' : 'INT4', \
		'db_size' : '4', \
		'form_size' : '4', \
		'default' : '0', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 4, \
		'required' : 1, \
		'validation_routine' : 'valid_integer', \
		'validation_arguments' : ['form.quantity_sold',"''","'Quantity Sold'","true"], \
		'leaveFocus' : "checkBlankField(this, 'Quantity Sold')", \
		'gainFocus' : "displayHint('Enter quantity sold')", \
		'format' : "####" \
		}, \
	    'keep_on_hand' : { \
		'label' : 'Keep On Hand', \
		'type' : 'INT4', \
		'db_size' : '4', \
		'form_size' : '4', \
		'default' : '0', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 5, \
		'required' : 1, \
		'validation_routine' : 'valid_integer', \
		'validation_arguments' : ['form.keep_on_hand',"''","'Keep on Hand'","true"], \
		'leaveFocus' : "checkBlankField(this, 'Keep on Hand')", \
		'gainFocus' : "displayHint('Enter the number of items to keep in stock')", \
		'format' : "####" \
		}, \
	    'description' : { \
		'label' : 'Description', \
		'type' : 'VARCHAR', \
		'db_size' : '40', \
		'form_size' : '40', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 6, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.description',"'Description'"], \
		'leaveFocus' : "checkBlankField(this, 'Description')", \
		'gainFocus' : "displayHint('Enter description of product')" \
		}, \
	    'price' : { \
		'label' : 'Price', \
		'type' : 'DECIMAL', \
		'db_size' : '9,2', \
		'form_size' : '10', \
		'default' : '0.00', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 7, \
		'required' : 1, \
		'validation_routine' : 'valid_money', \
		'validation_arguments' : ['form.price',"''","'Price'","true"], \
		'leaveFocus' : "checkBlankField(this, 'Price')", \
		'gainFocus' : "displayHint('Enter the price of product')", \
		'format' : "#######.##" \
		}, \
	    'shipping_weight' : { \
		'label' : 'Shipping Weight', \
		'type' : 'INT4', \
		'db_size' : '4', \
		'form_size' : '4', \
		'default' : '0', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 8, \
		'required' : 1, \
		'validation_routine' : 'valid_integer', \
		'validation_arguments' : ['form.shipping_weight',"''","'Shipping Weight'","true"], \
		'leaveFocus' : "checkBlankField(this, 'Shipping Weight')", \
		'gainFocus' : "displayHint('Enter the shipping weight of item')", \
		'format' : "####" \
		}, \
	    'image' : { \
		'label' : 'Product Image Filename', \
		'type' : 'VARCHAR', \
		'db_size' : '128', \
		'form_size' : '128', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 9, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.image',"'Product Image Filename'"], \
		'leaveFocus' : "checkBlankField(this, 'Product Picture')", \
		'gainFocus' : "displayHint('Enter the image filename of the products picture')" \
		}, \
	    'literature' : { \
		'label' : 'Literature Filename', \
		'type' : 'VARCHAR', \
		'db_size' : '128', \
		'form_size' : '128', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 10, \
		'required' : 1, \
		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.literature',"'Product Literature Filename'"], \
		'leaveFocus' : "checkBlankField(this, 'Product Literature')", \
		'gainFocus' : "displayHint('Enter the filename for the product literature page')" \
		}}, \
	'properties' : { \
	    'id' : { \
		'label' : 'Property Id', \
		'type' : 'VARCHAR', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'read-only', \
		'value' : '', \
		'display_order' : 1, \
		'required' : 1, \
		'leaveFocus' : "checkBlankField(this, 'Id')", \
		'gainFocus' : "displayHint('Enter the id of the property')" \
		}, \
	    'customer_id' : { \
		'label' : 'Customer Id', \
		'type' : 'VARCHAR', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 2, \
		'required' : 1, \
 		'validation_routine' : 'valid_integer', \
		'validation_arguments' : ['form.customer_id',"''","'Customer Id'","true"], \
		'leaveFocus' : "checkBlankField(this, 'Customer Id')", \
		'gainFocus' : "displayHint('Enter the customer id')" \
		}, \
	    'order_id' : { \
		'label' : 'Order Id', \
		'type' : 'VARCHAR', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 3, \
		'required' : 1, \
 		'validation_routine' : 'valid_integer', \
		'validation_arguments' : ['form.order_id',"''","'Order Id'","true"], \
		'leaveFocus' : "checkBlankField(this, 'Order Id')", \
		'gainFocus' : "displayHint('Enter the order id')" \
		}, \
	    'town' : { \
		'label' : 'Town', \
		'type' : 'VARCHAR', \
		'db_size' : '25', \
		'form_size' : '25', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 4, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.town',"'Town'"], \
		'leaveFocus' : "checkBlankField(this, 'Town')", \
		'gainFocus' : "displayHint('Enter the town that property is in')" \
		}, \
	    'subdivision' : { \
		'label' : 'Subdivision', \
		'type' : 'VARCHAR', \
		'db_size' : '20', \
		'form_size' : '20', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 5, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the subdivision')" \
		}, \
	    'style' : { \
		'label' : 'Style', \
		'type' : 'VARCHAR', \
		'db_size' : '20', \
		'form_size' : '20', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 6, \
		'leaveFocus' : "checkBlankField(this, 'Style')", \
		'gainFocus' : "displayHint('Enter the style')" \
		}, \
	    'bedrooms' : { \
		'label' : 'Bedrooms', \
		'type' : 'INT4', \
		'db_size' : '4', \
		'form_size' : '4', \
		'default' : '0', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 7, \
		'required' : 1, \
		'validation_routine' : 'valid_integer', \
		'validation_arguments' : ['form.bedrooms',"''","'Bedrooms'","true"], \
		'leaveFocus' : "checkBlankField(this, 'Bedrooms')", \
		'gainFocus' : "displayHint('Enter number of bedrooms')", \
		'format' : "####" \
		}, \
	    'baths' : { \
		'label' : 'Baths', \
		'type' : 'FLOAT4', \
		'db_size' : '4', \
		'form_size' : '4', \
		'default' : '0.0', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 8, \
		'required' : 1, \
		'validation_routine' : 'valid_float', \
		'validation_arguments' : ['form.baths',"''","'Baths'","true"], \
		'leaveFocus' : "checkBlankField(this, 'Baths')", \
		'gainFocus' : "displayHint('Enter number of baths')", \
		'format' : "##.#" \
		}, \
	    'square_footage' : { \
		'label' : 'Square Footage', \
		'type' : 'INT4', \
		'db_size' : '4', \
		'form_size' : '5', \
		'default' : '0', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 9, \
		'required' : 1, \
		'validation_routine' : 'valid_integer', \
		'validation_arguments' : ['form.square_footage',"''","'Square Footage'","true"], \
		'leaveFocus' : "checkBlankField(this, 'Square Footage')", \
		'gainFocus' : "displayHint('Enter the square footage')", \
		'format' : "#####" \
		}, \
	    'price' : { \
		'label' : 'Price', \
		'type' : 'DECIMAL', \
		'db_size' : '9,2', \
		'form_size' : '10', \
		'default' : '0.00', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 10, \
		'required' : 1, \
		'validation_routine' : 'valid_money', \
		'validation_arguments' : ['form.price',"''","'Price'","true"], \
		'leaveFocus' : "checkBlankField(this, 'Price')", \
		'gainFocus' : "displayHint('Enter the price')", \
		'format' : "#######.##" \
		}, \
	    'description' : { \
		'label' : 'Description', \
		'type' : 'VARCHAR', \
		'db_size' : '512', \
		'form_size' : '512', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 11, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.description',"'Description'"], \
		'leaveFocus' : "checkBlankField(this, 'Description')", \
		'gainFocus' : "displayHint('Enter the description')" \
		}, \
	    'image' : { \
		'label' : 'Image Filename', \
		'type' : 'VARCHAR', \
		'db_size' : '128', \
		'form_size' : '128', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 12, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the propertys image filename')" \
		}, \
	    'directions' : { \
		'label' : 'Directions', \
		'type' : 'VARCHAR', \
		'db_size' : '256', \
		'form_size' : '256', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 13, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.directions',"'Directions'"], \
		'leaveFocus' : "checkBlankField(this, 'Directions')", \
		'gainFocus' : "displayHint('Enter the directions to the property')" \
		}, \
	    'heating_air' : { \
		'label' : 'HVAC', \
		'type' : 'VARCHAR', \
		'db_size' : '30', \
		'form_size' : '30', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 14, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.heating_air',"'HVAC'"], \
		'leaveFocus' : "checkBlankField(this, 'Heating/Air Conditioning')", \
		'gainFocus' : "displayHint('Enter details about the heating/air conditioning')" \
		}, \
	    'number_rooms' : { \
		'label' : 'Number Rooms', \
		'type' : 'INT4', \
		'db_size' : '4', \
		'form_size' : '4', \
		'default' : '0', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 15, \
		'required' : 1, \
 		'validation_routine' : 'valid_integer', \
		'validation_arguments' : ['form.number_rooms',"''","'Number Rooms'","true"], \
		'leaveFocus' : "checkBlankField(this, 'Number of Rooms')", \
		'gainFocus' : "displayHint('Enter the number of rooms at property')", \
		'format' : "####" \
		}, \
	    'car_garage' : { \
		'label' : 'Number Car Garage', \
		'type' : 'INT4', \
		'db_size' : '4', \
		'form_size' : '4', \
		'display' : 'editable', \
		'default' : '0', \
		'value' : '', \
		'display_order' : 16, \
 		'validation_routine' : 'valid_integer', \
		'validation_arguments' : ['form.car_garage',"''","'Number Car Garage'","false"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the number of cars that can be parked in the garage')", \
		'format' : "####" \
		}, \
	    'date_built' : { \
		'label' : 'Date Built', \
		'type' : 'DATE', \
		'db_size' : '4', \
		'form_size' : '10', \
		'display' : 'editable', \
		'default' : None, \
		'value' : '', \
		'display_order' : 17, \
		'validation_routine' : 'valid_date', \
		'validation_arguments' : ['form.date_built',"'Date Built'","false"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the date the property was built')", \
		'format' : "MM-DD-YYYY" \
		}, \
	    'full_basement' : { \
		'label' : 'Full Basement', \
		'type' : 'BOOL', \
		'db_size' : '1', \
		'form_size' : '3', \
		'display' : 'editable', \
		'default' : 'f', \
		'value' : '', \
		'display_order' : 18, \
		'required' : 1, \
		'leaveFocus' : "checkBlankField(this, 'Full Basement')", \
		'gainFocus' : "displayHint('Select Yes/No if property has a full basement')" \
		}, \
	    'electric_service' : { \
		'label' : 'Electric Service', \
		'type' : 'VARCHAR', \
		'db_size' : '10', \
		'form_size' : '10', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 19, \
		'required' : 1, \
 		'validation_routine' : 'checkBlankField', \
		'validation_arguments' : ['form.electric_service',"'Electric Service'"], \
		'leaveFocus' : "checkBlankField(this, 'Electric Service')", \
		'gainFocus' : "displayHint('Enter the type of electric service 100/200 amp, etc.')" \
		}, \
	    'school_district' : { \
		'label' : 'School District', \
		'type' : 'VARCHAR', \
		'db_size' : '25', \
		'form_size' : '25', \
		'default' : None, \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 20, \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the school district that property is located in')" \
		}, \
	    'market_status' : { \
		'label' : 'Market Status', \
		'type' : 'VARCHAR', \
		'db_size' : '25', \
		'form_size' : '25', \
		'display' : 'editable', \
		'default' : None, \
		'value' : '', \
		'display_order' : 21, \
		'required' : 1, \
		'leaveFocus' : "checkBlankField(this, 'Market Status')", \
		'gainFocus' : "displayHint('Enter market status')", \
		'lov' : "SELECT status_of_market FROM market_status_values ORDER BY status_of_market" \
		}, \
	    'acreage' : { \
		'label' : 'Acreage', \
		'type' : 'FLOAT4', \
		'db_size' : '4', \
		'form_size' : '6', \
		'default' : '0.0', \
		'display' : 'editable', \
		'value' : '', \
		'display_order' : 22, \
		'validation_routine' : 'valid_float', \
		'validation_arguments' : ['form.acreage',"''","'Acreage'","false"], \
		'leaveFocus' : None, \
		'gainFocus' : "displayHint('Enter the acreage at the property')", \
		'format' : "####.#" \
		}, \
	    'display_property' : { \
		'label' : 'Display Property', \
		'type' : 'BOOL', \
		'db_size' : '1', \
		'form_size' : '3', \
		'display' : 'editable', \
		'default' : 'f', \
		'value' : '', \
		'display_order' : 23, \
		'required' : 1, \
		'leaveFocus' : "checkBlankField(this, 'Display Property Ad')", \
		'gainFocus' : "displayHint('Select Yes/No if property ad should be displayed')" \
		}} \
	}

    return data_tables
