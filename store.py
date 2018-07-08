# $Id: store.py,v 1.9 2000/04/16 23:14:43 davis Exp davis $
# Copyright (C) 1999 LinuXden, All Rights Reserved
# Copright Statement at http://www.linuxden.com/copyrighted_apps.html
# 
import os, string, sys
import cgi, glob
import time_pkg
from pg import DB
import ecommerce
import declarations
import Cookie

def store_front():
	ecommerce.htmlContentType(shopping_cart)

	table_data = declarations.define_tables()
		
def view_cart(shopping_cart):

	ecommerce.htmlContentType(shopping_cart)

	if shopping_cart == None:
		try:
			shopping_cart = Cookie.Cookie()
			shopping_cart.load(os.environ['HTTP_COOKIE'])
		except KeyError:
			shopping_cart = None

	table_data = declarations.define_tables()
	
	print "<HTML>"
	print "<HEAD>"

	if shopping_cart != None:
		
		# attempt to connect to db
		dbResult = ecommerce.connectDB(
			declarations.store_info['browser_username'],
			declarations.store_info['browser_password'],
			declarations.store_info['db_name'])
		
		# if db connection failed
		if dbResult['status'] != 'success':
			
			# generate appropriate message in alerts area
			ecommerce.alertsArea(form,"Can not view cart, could not connect to db,\n" + dbResult['message'])			
			
			# else db connection succeeded
		else:
			
			# assign db connection variable
			db = dbResult['result']

			item_list = []

			for i in shopping_cart.keys():
				if i[:4] == 'item':
					item_description = string.splitfields(shopping_cart[i].value,',')
					if item_description[1] != 'delete':
						item_list.append(i)

			j = 1

			validate_fields = {}
			validate_fields['store'] = {}

			for i in item_list:

				item_description = string.splitfields(shopping_cart[i].value,',')

				validate_fields['store']['qty_' + item_description[0]] = {
					'label' : 'Item ' + item_description[0] + ' Quantity', \
					'type' : 'INT4', \
					'db_size' : '4', \
					'form_size' : '3', \
					'default' : '0', \
					'display' : 'editable', \
					'value' : '', \
					'display_order' : j, \
					'validation_routine' : 'valid_integer', \
					'validation_arguments' : ['document.store.qty_' + item_description[0],"''","'Item Quantity'","true"], \
					}
				j = j + 1

			ecommerce.generate_form_javascript(validate_fields,'store','store',0,0)
			
			ecommerce.title("On-Line Store")
			
			print "</HEAD>" 
			
			ecommerce.bodySetup()
			
			ecommerce.mainHeading('On-Line Store')
			
			ecommerce.subHeading('View Cart')
	
			ecommerce.formSetup("store","store","return submitForm(document.store)",declarations.store_info['db_name'])

			item_list = []

			for i in shopping_cart.keys():

				if i[:4] == 'item':
					item_description = string.splitfields(shopping_cart[i].value,',')
					if item_description[1] != 'delete':
						item_list.append(i)

			if len(item_list) > 0:
				print "<TABLE BORDER=1>"
				print '<TR><TH><FONT FACE="Arial,Helvetica" SIZE="-1">Code</FONT></TH><TH><FONT FACE="Arial,Helvetica" SIZE="-1">Image</FONT></TH><TH><FONT FACE="Arial,Helvetica" SIZE="-1">Description</FONT></TH><TH><FONT FACE="Arial,Helvetica" SIZE="-1">Weight</FONT></TH><TH><FONT FACE="Arial,Helvetica" SIZE="-1">Qty</FONT></TH><TH><FONT FACE="Arial,Helvetica" SIZE="-1">Price</FONT></TH><TH><FONT FACE="Arial,Helvetica" SIZE="-1">Total</FONT></TH></TR>'
			
				orderTotal = 0.0
				quantityTotal = 0
				weightTotal = 0
			
			for i in item_list:

				item_description = string.splitfields(shopping_cart[i].value,',')
				
				dbResult = ecommerce.executeSQL(
					db, 
					"SELECT id, image, description, shipping_weight, price, literature FROM products WHERE id = '" + item_description[0] + "'")
				
				if dbResult['status'] != 'success':
					
					ecommerce.alertsArea(form, "Could not select products\n" + dbResult['message'])
						
				else:
					
					result = dbResult['result']
					
					table_data = ecommerce.dbToTableData(table_data, 'products', result[0])
					
					if string.atoi(item_description[1]) > 0:
						
						quantityTotal = quantityTotal + string.atoi(item_description[1])
						print '<TR>'
						
						ecommerce.tableColumn(table_data['products']['id']['value'])
						
						print '<TD ALIGN=CENTER NOWRAP>'
						ecommerce.image(
							image_name=table_data['products']['image']['value'],
							store_name=declarations.store_info['db_name'])
							
						print '</TD>'
						
						print '<TD ALIGN=CENTER NOWRAP>'				
						ecommerce.urlhref('/' + table_data['products']['literature']['value'],'<FONT FACE="Arial,Helvetica" SIZE="-1">' + table_data['products']['description']['value'] + '</FONT>')
						print '</TD>'
						
						print '<TD ALIGN=CENTER NOWRAP><FONT FACE="Arial,Helvetica" SIZE="-1">'
						
						if table_data['products']['shipping_weight']['value'] != 0:
							weightTotal = weightTotal + int(table_data['products']['shipping_weight']['value'])
							print table_data['products']['shipping_weight']['value']
								
						else:

							print "N/A"
							
						print '</FONT></TD>'
								
						print '<TD ALIGN=CENTER NOWRAP><FONT FACE="Arial,Helvetica" SIZE="-1">'
						
						ecommerce.textbox('products',
								'qty_' + table_data['products']['id']['value'],
								item_description[1],
								'3',
								'3',
								None,
								None)
						
						print '</FONT></TD>'
						
						ecommerce.tableColumn('$ ' + table_data['products']['price']['value'])
						
						lineTotal = string.atoi(item_description[1]) * string.atof(table_data['products']['price']['value'])
						
						ecommerce.tableColumn("$ %9.2f" % lineTotal)
						
						orderTotal = orderTotal + lineTotal
						
						print '<TD ALIGN=CENTER NOWRAP><FONT FACE="Arial,Helvetica" SIZE="-1"><INPUT NAME="changeitem" type="button" value=" Change " onClick="return execute(' + "'changeitem'" + ", '" + table_data['products']['id']['value'] + "'" + ')"></FONT></TD>'
						print '<TD ALIGN=CENTER NOWRAP><FONT FACE="Arial,Helvetica" SIZE="-1"><INPUT NAME="removeitem" type="button" value=" Remove " onClick="return execute(' + "'removeitem'" + ", '" + table_data['products']['id']['value'] + "'" + ')"></FONT></TD>'
						
						print '</TR>'
				
			if len(item_list) > 0:
				print '<TR><TD COLSPAN=3></TD><TD ALIGN=CENTER><FONT FACE="Arial,Helvetica" SIZE="-1">' + `weightTotal` + '</FONT></TD><TD ALIGN=CENTER><FONT FACE="Arial,Helvetica" SIZE="-1">' + `quantityTotal` + '</FONT></TD><TD></TD><TD ALIGN=CENTER><FONT FACE="Arial,Helvetica" SIZE="-1">$ ' + "%9.2f" % orderTotal + '</FONT></TD></TR>'
				print "</TABLE>"

				ecommerce.alertsArea(form, "Shopping cart items retrieved successfully")
			else:
				ecommerce.alertsArea(form, "No items in shopping cart")

	
	else:

		ecommerce.javaScript('store')

		ecommerce.title("On-Line Store")
		
		print "</HEAD>" 
		
		ecommerce.bodySetup()
		
		ecommerce.mainHeading('On-Line Store')
		
		ecommerce.subHeading('View Cart')
		
		ecommerce.formSetup("store","store","return submitForm(document.store)",declarations.store_info['db_name'])

		ecommerce.alertsArea(form, "No items in shopping cart")
			
	print '<TABLE>'
	print '<TR>'
	print '<TD ALIGN=CENTER NOWRAP><FONT FACE="Arial,Helvetica" SIZE="-1"><INPUT NAME="store" type="button" value=" Continue Shopping " onClick="return execute(' + "'shop'" + ')"></FONT></TD>'

	if shopping_cart != None and len(item_list) > 0:
		print '<TD ALIGN=CENTER NOWRAP><FONT FACE="Arial,Helvetica" SIZE="-1"><INPUT NAME="checkout" type="button" value=" Check Out " onClick="return execute(' + "'checkout'" + ')"></FONT></TD>'

	print '</TR></TABLE>'

	ecommerce.storeHiddenFields(form["uHidden"].value, form["pHidden"].value)
		
	print "</FORM>"

	try:
		ecommerce.trailer(table_data, db)
		db.close()
	except NameError:
		pass

	print "</BODY>"
	print "</HTML>"

def product_listing(shopping_cart):

	# first invocation of store page
	table_data = declarations.define_tables()

	ecommerce.htmlContentType(shopping_cart)

	print "<HTML>"
	print "<HEAD>"

	dbResult = ecommerce.connectDB(
		declarations.store_info['browser_username'],
		declarations.store_info['browser_password'],
		declarations.store_info['db_name'])
	
	# if db connection failed
	if dbResult['status'] != 'success':
		
		# generate appropriate message in alerts area
		ecommerce.alertsArea(form,"Can not list products, could not connect to db,\n" + dbResult['message'])			
		
	# else db connection succeeded
	else:

		# assign db connection variable
		db = dbResult['result']
		
		dbResult = ecommerce.executeSQL(db, "SELECT id, image, description, price, literature FROM products ORDER BY id")
		
		if dbResult['status'] != 'success':
			
			ecommerce.alertsArea(form, "Could not select products\n" + dbResult['message'])
			
		else:
			
			result = dbResult['result']

			validate_fields = {}
			validate_fields['store'] = {}

			for i in xrange(0,len(result)):

				table_data = ecommerce.dbToTableData(table_data, 'products', result[i])

				validate_fields['store']['qty_' + table_data['products']['id']['value']] = {
					'label' : 'Item ' + table_data['products']['id']['value'] + ' Quantity', \
					'type' : 'INT4', \
					'db_size' : '4', \
					'form_size' : '3', \
					'default' : '0', \
					'display' : 'editable', \
					'value' : '', \
					'display_order' : i+1, \
					'validation_routine' : 'valid_integer', \
					'validation_arguments' : ['document.store.qty_' + table_data['products']['id']['value'],"''","'Item Quantity'","true"], \
					}
	
			ecommerce.generate_form_javascript(validate_fields,'store','store',0,0)
		
			ecommerce.title("On-Line Store")
			
			print "</HEAD>" 
			
			ecommerce.bodySetup()

			print '<CENTER>'
			print '<TABLE COLS=1 WIDTH=585>'
			print '<TR><TD>'

			ecommerce.mainHeading('On-Line Store')
			
			ecommerce.subHeading('Products')
			
			ecommerce.formSetup("store","store","return submitForm(document.store)",declarations.store_info['db_name'])

			print "<TABLE BORDER=1>"
			
			print '<TR><TH><FONT FACE="Arial,Helvetica" SIZE="-1">Code</FONT></TH><TH><FONT FACE="Arial,Helvetica" SIZE="-1">Image</FONT></TH><TH><FONT FACE="Arial,Helvetica" SIZE="-1">Description</FONT></TH><TH><FONT FACE="Arial,Helvetica" SIZE="-1">Qty</FONT></TH><TH><FONT FACE="Arial,Helvetica" SIZE="-1">Price</FONT></TH></TR>'
			
			for i in xrange(0,len(result)):
				
				table_data = ecommerce.dbToTableData(table_data, 'products', result[i])
				
				print '<TR>'
				
				ecommerce.tableColumn(table_data['products']['id']['value'])
				
				print '<TD ALIGN=CENTER NOWRAP>'
				ecommerce.image(
					image_name=table_data['products']['image']['value'],
					store_name=declarations.store_info['db_name'])
				print '</TD>'
				
				print '<TD ALIGN=CENTER NOWRAP>'				
				ecommerce.urlhref('/' + table_data['products']['literature']['value'], '<FONT FACE="Arial,Helvetica" SIZE="-1">' + table_data['products']['description']['value'] + '</FONT>')
				print '</TD>'

				print '<TD ALIGN=CENTER NOWRAP><FONT FACE="Arial,Helvetica" SIZE="-1">'
				ecommerce.textbox('products',
								  'qty_' + table_data['products']['id']['value'],
								  '0',
								  '3',
								  '3',
								  None,
								  None)
				
				print '</FONT></TD>'

				ecommerce.tableColumn('$ ' + table_data['products']['price']['value'])

				print '<TD ALIGN=CENTER NOWRAP><FONT FACE="Arial,Helvetica" SIZE="-1"><INPUT NAME="addtocart" type="button" value=" Add to Cart " onClick="return execute(' + "'addtocart'" + ",'" + table_data['products']['id']['value'] + "'" + ')">'

				print '</FONT></TD>'

				print '</TR>'
				
			print "</TABLE>"
				
			print "<TABLE BORDER=0>"


	ecommerce.storeFunctions()

	ecommerce.storeHiddenFields(
		declarations.store_info['browser_username'],
		declarations.store_info['browser_password'])

	print "</FORM>"

	try:
		ecommerce.trailer(table_data, db)
		db.close()
	except NameError:
		pass
		
	print '</TD>'
	print '</TR>'
	print '</TABLE>'
	print '</CENTER>'
	print "</BODY>"
	print "</HTML>"

form = ecommerce.getFormData()

if form.has_key("action"):

	if form["action"].value == "removeitem":

		shopping_cart_empty = 1
		try:
			shopping_cart = Cookie.Cookie()
			shopping_cart.load(os.environ['HTTP_COOKIE'])
			shopping_cart_empty = 0
		except KeyError:
			shopping_cart = Cookie.Cookie()

		if shopping_cart_empty:
			num_items = 0
		else:
			num_items = int(shopping_cart['num_items'].value)

		for i in shopping_cart.keys():

			if i[:4] != 'item':
				continue

			item_description = string.splitfields(shopping_cart[i].value,',')

			if item_description[0] == form['key_id'].value:
				# remove from shopping cart cookie
				shopping_cart[i] = "%s,%s" % ("pending","delete")
				shopping_cart[i]['expires'] = -60000
				shopping_cart['num_items'] = `num_items-1`

		view_cart(shopping_cart)

	if form["action"].value == "changeitem":

		shopping_cart_empty = 1
		try:
			shopping_cart = Cookie.Cookie()
			shopping_cart.load(os.environ['HTTP_COOKIE'])
			shopping_cart_empty = 0
		except KeyError:
			shopping_cart = Cookie.Cookie()

		for i in shopping_cart.keys():

			if i[:4] != 'item':
				continue

			item_description = string.splitfields(shopping_cart[i].value,',')

			if item_description[0] == form['key_id'].value:
				shopping_cart[i] = "%s,%s" % (form['key_id'].value,`int(form['qty_' + form['key_id'].value].value)`)

		view_cart(shopping_cart)

	if form["action"].value == "addtocart":

		shopping_cart_empty = 1

		try:
			shopping_cart = Cookie.Cookie()
			shopping_cart.load(os.environ['HTTP_COOKIE'])
			shopping_cart_empty = 0
		except KeyError:
			shopping_cart = Cookie.Cookie()

		if shopping_cart_empty:
			num_items = 0
		else:
			if shopping_cart.has_key('num_items'):
				num_items = int(shopping_cart['num_items'].value)
			else:
				num_items = 0

		if string.strip(form['qty_' + form['key_id'].value].value) != '0':

			found_item_in_cart = 0

			# see if item is already in cart
			for i in shopping_cart.keys():
				
				if i[:4] != 'item':
					continue

				item_description = string.splitfields(shopping_cart[i].value,',')

				if item_description[0] == form['key_id'].value:
					# customer adding an item which is already in cart
					# so just modify this item
					shopping_cart[i] = "%s,%s" % (form['key_id'].value,`int(form['qty_' + form['key_id'].value].value)`)
					found_item_in_cart = 1
					break

			if not found_item_in_cart:
				# add the item to the cart
				shopping_cart['item' + `num_items + 1`] = form['key_id'].value + "," + form['qty_' + form['key_id'].value].value

				shopping_cart['num_items'] = `num_items + 1`

		else:
			if num_items == 0:
				shopping_cart = None

		product_listing(shopping_cart)

	if form["action"].value == "viewcart":
		view_cart(None)
	
	elif form["action"].value == "shop":

		shopping_cart_empty = 1
		try:
			shopping_cart = Cookie.Cookie()
			shopping_cart.load(os.environ['HTTP_COOKIE'])
			shopping_cart_empty = 0
		except KeyError:
			shopping_cart = Cookie.Cookie()

		product_listing(shopping_cart)

	elif form["action"].value == "checkout":

		try:
			shopping_cart = Cookie.Cookie()
			shopping_cart.load(os.environ['HTTP_COOKIE'])
			num_items = int(shopping_cart['num_items'].value)
		except KeyError:
			shopping_cart = None
			num_items = 0

		ecommerce.htmlContentType(shopping_cart)

		table_data = declarations.define_tables()

		print "<HTML>"
		print "<HEAD>"
		
		if num_items == 0:
			javaScript('store')
		else:
			ecommerce.generate_form_javascript(table_data,'customers','store',0,0)
		
		ecommerce.title("On-Line Store")
		
		print "</HEAD>" 
		
		ecommerce.bodySetup()

		ecommerce.mainHeading('On-Line Store')
		
		ecommerce.subHeading('Check Out')
			
		ecommerce.formSetup("store","store","return submitForm(document.store)",declarations.store_info['db_name'])

		if num_items == 0:
			ecommerce.alertsArea(form,"You do not have any items in your shopping cart")

			print '<TABLE>'
			print '<TR>'
			print '<TD ALIGN=CENTER NOWRAP><FONT FACE="Arial,Helvetica" SIZE="-1"><INPUT NAME="store" type="button" value=" Continue Shopping " onClick="return execute(' + "'shop'" + ')"></FONT></TD>'
			print '</TR></TABLE>'

		else:
			ecommerce.printText('Please enter the following information:<BR>Note: For address information, provide your billing address<BR>')

			table_data['customers']['id']['display'] = 'Hidden'

			# attempt to connect to db
			dbResult = ecommerce.connectDB(
				declarations.store_info['browser_username'],
				declarations.store_info['browser_password'],
				declarations.store_info['db_name'])
			
			# if db connection failed
			if dbResult['status'] != 'success':
			
				# generate appropriate message in alerts area
				ecommerce.alertsArea(form,"Can not connect to database\n" + dbResult['message'])
			
			else:
				
				# assign db connection variable
				db = dbResult['result']

				ecommerce.display_form(table_data,'customers',1,'useValues',1,db)

			print '<TABLE>'
			print '<TR>'
			print '<TD ALIGN=CENTER NOWRAP><FONT FACE="Arial,Helvetica" SIZE="-1"><INPUT NAME="store" type="button" value=" Continue " onClick="return execute(' + "'order'" + ')"></FONT></TD>'
			print '</TR></TABLE>'

		ecommerce.storeHiddenFields(form["uHidden"].value, form["pHidden"].value)
		
		print "</FORM>"

		try:
			ecommerce.trailer(table_data, db)
			db.close()
		except NameError:
			pass

		print "</BODY>"
		print "</HTML>"

	elif form["action"].value == "order":

		try:
			shopping_cart = Cookie.Cookie()
			shopping_cart.load(os.environ['HTTP_COOKIE'])
			num_items = int(shopping_cart['num_items'].value)
		except KeyError:
			shopping_cart = None
			num_items = 0

		# load cookie with customer data fields
		table_data = declarations.define_tables()

		ecommerce.htmlContentType(None)

		print "<HTML>"
		print "<HEAD>"

		table_data['orders']['id']['display'] = 'Hidden'
		table_data['orders']['customer_id']['display'] = 'Hidden'
		table_data['orders']['creation_date']['display'] = 'Hidden'
		table_data['orders']['shipped_date']['display'] = 'Hidden'
		table_data['orders']['processor']['display'] = 'Hidden'
		table_data['orders']['shipping_handling']['display'] = 'Hidden'
		table_data['orders']['subtotal']['display'] = 'Hidden'
		table_data['orders']['total']['display'] = 'Hidden'
		table_data['orders']['order_status']['display'] = 'Hidden'
		table_data['orders']['tracking_number']['display'] = 'Hidden'
		table_data['orders']['sales_tax']['display'] = 'Hidden'

		ecommerce.generate_form_javascript(table_data,'orders','store',0,0)
		
		ecommerce.title("On-Line Store")
		
		print "</HEAD>" 
		
		ecommerce.bodySetup()

		ecommerce.mainHeading('On-Line Store')
		
		ecommerce.subHeading('Check Out')
			
		ecommerce.formSetup("store","store","return submitForm(document.store)",declarations.store_info['db_name'])

		if num_items == 0:
			ecommerce.alertsArea(form,"You do not have any items in your shopping cart")

			print '<TABLE>'
			print '<TR>'
			print '<TD ALIGN=CENTER NOWRAP><FONT FACE="Arial,Helvetica" SIZE="-1"><INPUT NAME="store" type="button" value=" Continue Shopping " onClick="return execute(' + "'shop'" + ')"></FONT></TD>'
			print '</TR></TABLE>'

		else:
			ecommerce.printText('Please enter the following information:<BR>Note: For address information, provide the address to ship to even if it is the same as billing address.<BR>')

			table_data['orders']['shipping_street1']['value'] = form['street_1'].value
			table_data['orders']['shipping_street2']['value'] = form['street_2'].value
			table_data['orders']['city']['value'] = form['city'].value
			table_data['orders']['state']['value'] = form['state'].value
			table_data['orders']['zip']['value'] = form['zip'].value

			dbResult = ecommerce.connectDB(
				declarations.store_info['browser_username'],
				declarations.store_info['browser_password'],
				declarations.store_info['db_name'])
			
			# if db connection failed
			if dbResult['status'] != 'success':
			
				# generate appropriate message in alerts area
				ecommerce.alertsArea(form,"Can not connect to database\n" + dbResult['message'])
			
			else:
				
				# assign db connection variable
				db = dbResult['result']

				ecommerce.display_form(table_data,'orders',1,'useValues',1,db)


			print '<TABLE>'
			print '<TR>'
			print '<TD ALIGN=CENTER NOWRAP><FONT FACE="Arial,Helvetica" SIZE="-1"><INPUT NAME="store" type="button" value=" Continue " onClick="return execute(' + "'purchase'" + ')"></FONT></TD>'
			print '</TR></TABLE>'

		ecommerce.storeHiddenFields(form["uHidden"].value, form["pHidden"].value)
		ecommerce.formToHiddenFields(table_data,'customers',form)

		print "</FORM>"

		ecommerce.trailer(table_data, db)
		db.close()

		print "</BODY>"
		print "</HTML>"

	elif form["action"].value == "purchase" or form['action'].value == 'place_order':

		properties_to_insert = 0

		try:
			shopping_cart = Cookie.Cookie()
			shopping_cart.load(os.environ['HTTP_COOKIE'])
			num_items = int(shopping_cart['num_items'].value)
		except KeyError:
			shopping_cart = None
			num_items = 0

		table_data = declarations.define_tables()

		ecommerce.htmlContentType(None)

		print "<HTML>"
		print "<HEAD>"
		
		ecommerce.javaScript("store")
		
		ecommerce.title("On-Line Store")
		
		print "</HEAD>" 
		
		ecommerce.bodySetup()

		ecommerce.mainHeading('On-Line Store')
		
		ecommerce.subHeading('Check Out')
			
		ecommerce.formSetup("store","store","return submitForm(document.store)",declarations.store_info['db_name'])

		if num_items == 0:
			ecommerce.alertsArea(form,"You do not have any items in your shopping cart")

			print '<TABLE>'
			print '<TR>'
			print '<TD ALIGN=CENTER NOWRAP><FONT FACE="Arial,Helvetica" SIZE="-1"><INPUT NAME="store" type="button" value=" Continue Shopping " onClick="return execute(' + "'shop'" + ')"></FONT></TD>'
			print '</TR></TABLE>'

		else:
			if form['action'].value == 'purchase':
				ecommerce.printText('Please verify that the following information is correct.<BR>If any information is incorrect use the [Back] button to go back to previous screens to correct<BR><BR><CENTER>Depress the [Place Order] button to place your order.</CENTER>')
			else:
				ecommerce.printText('<B>Your order has been placed with the following information:</B>')


			ecommerce.hiddenFieldsWithTableNameToTableData(table_data,'customers',form)

			print '<TABLE>'
			print '<TR>'

			print '<TD>'
			ecommerce.printText('<B>Customer Information</B>')

			if form['action'].value == 'purchase':
				table_data['customers']['id']['display'] = 'Hidden'
			else:

				dbResult = ecommerce.connectDB(
					declarations.store_info['browser_username'],
					declarations.store_info['browser_password'],
					declarations.store_info['db_name'])
		
				# if db connection failed
				if dbResult['status'] != 'success':
			
					# generate appropriate message in alerts area
					ecommerce.alertsArea(form,"Can not connect to database\n" + dbResult['message'])
			
				else:
				
					# assign db connection variable
					db = dbResult['result']

					dbResult = ecommerce.executeSQL(db, "SELECT NEXTVAL('customer_id_seq')")
		
					if dbResult['status'] != 'success':
					
						ecommerce.alertsArea(form, "Could not retrieve next customer id\n" + dbResult['message'])
					
					else:
			
						result = dbResult['result']

						if result != []:
							customer_id = {'id' : `result[0]['nextval']`}

							table_data = ecommerce.dbToTableData(table_data, 'customers', customer_id)						

							if form['action'].value == 'place_order':
								
								# save the form from the table_data for customers
								dbResult = ecommerce.saveForm(table_data, db, table_data['customers']['id']['value'], "customers", " WHERE id = '" + table_data['customers']['id']['value'] + "'", form, 0, 0)

								# if the form was not successfully saved
								if dbResult['status'] != 'success':
									ecommerce.alertsArea(form,"Customer data could not be saved due to an error during save,\n" + dbResult['message'] )

						

			ecommerce.display_form(table_data,'customers',editable=0,displayOrder='useValues',displayHeader=0)

			if form['action'].value == 'place_order' and \
			   string.strip(table_data['customers']['email']['value']) != '':

				email_form = table_data['customers']['first_name']['value'] + ' ' + table_data['customers']['middle_initial']['value'] + '. ' + table_data['customers']['last_name']['value'] + ', an order has been placed for you.' + '\n'
				email_form = email_form + 'You will be notified via e-mail when your order has been shipped.' + '\n'
				email_form = email_form + '\n' + 'Visit http://www.clicktree.com for other great on-line stores.' + '\n\n'

				email_form = email_form + (80 * '-') + '\n'
				email_form = email_form + 'Customer Information:' + '\n\n'

				email_form = email_form + ecommerce.table_data_to_email(table_data,'customers')

			print '</TD>'
			print '<TD COLSPAN=2>'
			print '</TD>'
			print '<TD>'
			
			if form['action'].value == 'purchase':
				ecommerce.formToTableData(table_data,'orders',form)

				table_data['orders']['id']['display'] = 'Hidden'
				table_data['orders']['customer_id']['display'] = 'Hidden'
				table_data['orders']['creation_date']['display'] = 'Hidden'
				table_data['orders']['shipped_date']['display'] = 'Hidden'
				table_data['orders']['processor']['display'] = 'Hidden'
				table_data['orders']['tracking_number']['display'] = 'Hidden'
				table_data['orders']['order_status']['display'] = 'Hidden'
				table_data['orders']['shipping_handling']['display'] = 'Hidden'
				table_data['orders']['subtotal']['display'] = 'Hidden'
				table_data['orders']['total']['display'] = 'Hidden'
				table_data['orders']['sales_tax']['display'] = 'Hidden'
				
			else:

				ecommerce.hiddenFieldsWithTableNameToTableData(table_data,'orders',form)

				dbResult = ecommerce.connectDB(
					declarations.store_info['browser_username'],
					declarations.store_info['browser_password'],
					declarations.store_info['db_name'])
		
				# if db connection failed
				if dbResult['status'] != 'success':
			
					# generate appropriate message in alerts area
					ecommerce.alertsArea(form,"Can not connect to database\n" + dbResult['message'])
			
				else:
				
					# assign db connection variable
					db = dbResult['result']

					dbResult = ecommerce.executeSQL(db, "SELECT NEXTVAL('orders_id_seq')")
		
					if dbResult['status'] != 'success':
					
						ecommerce.alertsArea(form, "Could not retrieve next order id\n" + dbResult['message'])
					
					else:
			
						result = dbResult['result']

						if result != []:

							order_id = {'id' : `result[0]['nextval']`}

							table_data = ecommerce.dbToTableData(table_data, 'orders', order_id)						


				table_data['orders']['creation_date']['value'] = time_pkg.current_time_MM_DD_YYYY()
				table_data['orders']['customer_id']['display'] = 'Hidden'
				table_data['orders']['customer_id']['value'] = table_data['customers']['id']['value']
				table_data['orders']['shipped_date']['display'] = 'Hidden'
				table_data['orders']['processor']['display'] = 'Hidden'
				table_data['orders']['tracking_number']['display'] = 'Hidden'
				table_data['orders']['order_status']['display'] = 'Hidden'
				table_data['orders']['order_status']['value'] = 'Pending Card Approval'
				table_data['orders']['shipping_handling']['display'] = 'Hidden'
				table_data['orders']['subtotal']['display'] = 'Hidden'
				table_data['orders']['total']['display'] = 'Hidden'
				table_data['orders']['sales_tax']['display'] = 'Hidden'
				
			ecommerce.printText('<BR><B>Shipping and Credit Card Information</B>')

			ecommerce.display_form(table_data,'orders',editable=0,displayOrder='useValues',displayHeader=0)

			if form['action'].value == 'place_order' and \
			   string.strip(table_data['customers']['email']['value']) != '':

				email_form = email_form + (80 * '-') + '\n'
				email_form = email_form + '\nOrder Information:' + '\n\n'
				
				email_form = email_form + ecommerce.table_data_to_email(table_data,'orders')
				
			print '</TD>'
			print '</TR>'
			print '</TABLE>'

			if shopping_cart != None:

				dbResult = ecommerce.connectDB(
					declarations.store_info['browser_username'],
					declarations.store_info['browser_password'],
					declarations.store_info['db_name'])
		
				# if db connection failed
				if dbResult['status'] != 'success':
			
					# generate appropriate message in alerts area
					ecommerce.alertsArea(form,"Can not retrieve shopping cart data, could not connect to db,\n" + dbResult['message'])
			
				else:
				
					# assign db connection variable
					db = dbResult['result']

					item_list = []
					line_item = 0

					for i in shopping_cart.keys():

						if i[:4] == 'item':
							item_description = string.splitfields(shopping_cart[i].value,',')
							if item_description[1] != 'delete':
								item_list.append(i)

					if len(item_list) > 0:

						ecommerce.printText('<BR><B>Items Ordered</B>')

						print "<TABLE BORDER=1>"
						print '<TR><TH><FONT FACE="Arial,Helvetica" SIZE="-1">Code</FONT></TH><TH><FONT FACE="Arial,Helvetica" SIZE="-1">Image</FONT></TH><TH><FONT FACE="Arial,Helvetica" SIZE="-1">Description</FONT></TH><TH><FONT FACE="Arial,Helvetica" SIZE="-1">Weight</FONT></TH><TH><FONT FACE="Arial,Helvetica" SIZE="-1">Qty</FONT></TH><TH><FONT FACE="Arial,Helvetica" SIZE="-1">Price</FONT></TH><TH><FONT FACE="Arial,Helvetica" SIZE="-1">Total</FONT></TH></TR>'

						if form['action'].value == 'place_order' and \
						   string.strip(table_data['customers']['email']['value']) != '':
							
							email_form = email_form + (80 * '-') + '\n'
							email_form = email_form + '\nItems Ordered:' + '\n\n'

							email_form = email_form + string.rjust('Code',int(table_data['products']['id']['form_size'])) + '  ' + string.rjust('Description',int(table_data['products']['description']['form_size'])) + '  ' + string.rjust('Wght',int(table_data['products']['shipping_weight']['form_size'])) + '  ' + string.rjust('Qty',int(table_data['order_items']['quantity']['form_size'])) + '  ' + string.rjust('Price',int(table_data['order_items']['price']['form_size'])) + '  ' + string.rjust('Total',int(table_data['order_items']['line_subtotal']['form_size'])) + '\n\n'

						orderTotal = 0.0
						quantityTotal = 0
						weightTotal = 0
								
					for i in item_list:
						
						item_description = string.splitfields(shopping_cart[i].value,',')
						
						dbResult = ecommerce.executeSQL(db, "SELECT id, image, description, shipping_weight, price, literature FROM products WHERE id = '" + item_description[0] + "'")

						if dbResult['status'] != 'success':
					
							ecommerce.alertsArea(form, "Could not select products\n" + dbResult['message'])
							
						else:
							
							result = dbResult['result']
							
							table_data = ecommerce.dbToTableData(table_data, 'products', result[0])
							
							# START FSBO UNIQUE PROCESSING
							if table_data['products']['description']['value'][-2:] == 'Ad':
								properties_to_insert = properties_to_insert + string.atoi(item_description[1])

							# END FSBO UNIQUE PROCESSING

							if string.atoi(item_description[1]) > 0:
						
								quantityTotal = quantityTotal + string.atoi(item_description[1])
								print '<TR>'
								
								ecommerce.tableColumn(table_data['products']['id']['value'])
								
								print '<TD ALIGN=CENTER NOWRAP>'
								ecommerce.image(
									image_name=table_data['products']['image']['value'],
									store_name=declarations.store_info['db_name'])
								print '</TD>'
								
								print '<TD ALIGN=CENTER NOWRAP>'				
								ecommerce.urlhref('/' + table_data['products']['literature']['value'],'<FONT FACE="Arial,Helvetica" SIZE="-1">' + table_data['products']['description']['value'] + '</FONT>')
								print '</TD>'
								
								print '<TD ALIGN=CENTER NOWRAP><FONT FACE="Arial,Helvetica" SIZE="-1">'
								
								if table_data['products']['shipping_weight']['value'] != 0:
									weightTotal = weightTotal + (int(item_description[1]) * int(table_data['products']['shipping_weight']['value']))
									print table_data['products']['shipping_weight']['value']
								
								else:

									print "N/A"
							
								print '</FONT></TD>'
								
								print '<TD ALIGN=CENTER NOWRAP><FONT FACE="Arial,Helvetica" SIZE="-1">'
						
								print item_description[1]
						
								print '</FONT></TD>'
						
								ecommerce.tableColumn('$ ' + table_data['products']['price']['value'])
						
								lineTotal = string.atoi(item_description[1]) * string.atof(table_data['products']['price']['value'])
								
								ecommerce.tableColumn("$ %9.2f" % lineTotal)
								
								orderTotal = orderTotal + lineTotal

								if form['action'].value == 'place_order':

									line_item = line_item + 1
									
									table_data['order_items']['line_item']['value'] = `line_item`
									table_data['order_items']['order_id']['value'] = table_data['orders']['id']['value']
									table_data['order_items']['product_id']['value'] = table_data['products']['id']['value']
									table_data['order_items']['quantity']['value'] = item_description[1]
									table_data['order_items']['price']['value'] = table_data['products']['price']['value']
									table_data['order_items']['line_subtotal']['value'] = '%9.2f' % (lineTotal)
									if string.strip(table_data['customers']['email']['value']) != '':

										email_form = email_form + string.rjust(table_data['order_items']['product_id']['value'],int(table_data['order_items']['product_id']['form_size'])) + '  ' + string.rjust(table_data['products']['description']['value'],int(table_data['products']['description']['form_size'])) + '  ' + string.rjust(table_data['products']['shipping_weight']['value'],int(table_data['products']['shipping_weight']['form_size'])) + '  ' + string.rjust(table_data['order_items']['quantity']['value'],int(table_data['order_items']['quantity']['form_size'])) + '  ' + string.rjust(table_data['order_items']['price']['value'],int(table_data['order_items']['price']['form_size'])) + '  ' + string.rjust(table_data['order_items']['line_subtotal']['value'],int(table_data['order_items']['line_subtotal']['form_size'])) + '\n'

									dbResult = ecommerce.saveForm(table_data, db, None, "order_items", None, form, 0, 0, 1)

									# if the form was not successfully saved
									if dbResult['status'] != 'success':
										ecommerce.alertsArea(form,"Order items could not be saved due to an error during save,\n" + dbResult['message'] )

								print '</TR>'
				
					if len(item_list) > 0:
						print '<TR><TD COLSPAN=3></TD><TD ALIGN=CENTER><FONT FACE="Arial,Helvetica" SIZE="-1">' + `weightTotal` + '</FONT></TD><TD ALIGN=CENTER><FONT FACE="Arial,Helvetica" SIZE="-1">' + `quantityTotal` + '</FONT></TD><TD></TD><TD ALIGN=CENTER><FONT FACE="Arial,Helvetica" SIZE="-1">$ ' + "%9.2f" % orderTotal + '</FONT></TD></TR>'
						print "</TABLE>"
						
					ecommerce.printText('<BR><B>Order Summary</B>')

					print '<TABLE BORDER=1>'
					print '<TR>'
					ecommerce.tableColumn('<B>Subtotal:</B>','left')
					ecommerce.tableColumn('%10.2f' % (orderTotal),'right')
					print '</TR>'
					print '<TR>'
					ecommerce.tableColumn('<B>Shipping and Handling:</B>','left')
					ecommerce.tableColumn('0.00','right')
					print '</TR>'
					print '<TR>'
					ecommerce.tableColumn('<B>Sales Tax:</B>','left')

					dbResult = ecommerce.executeSQL(db, "SELECT tax FROM sales_tax_by_state WHERE state_abbreviation = '" + string.upper(form['customers_state_hidden'].value) + "'")
		
					if dbResult['status'] != 'success':
			
						ecommerce.alertsArea(form, "Could not charge tax based on state entered\n" + dbResult['message'])
			
					else:
			
						result = dbResult['result']

						if result != []:
							table_data = ecommerce.dbToTableData(table_data, 'sales_tax_by_state', result[0])
						else:
							table_data = ecommerce.dbToTableData(table_data, 'sales_tax_by_state', {'tax' : 0.00})

						tax = float(table_data['sales_tax_by_state']['tax']['value']) * float(orderTotal)

						ecommerce.tableColumn('%10.2f' % (tax),'right')

						print '</TR>'
						print '<TR>'
						ecommerce.tableColumn('<B>Total:</B>','left')
						ecommerce.tableColumn('%10.2f' % (orderTotal + tax),'right')
						print '</TR>'
						print '</TABLE>'

					if form['action'].value == 'purchase':
						print '<TABLE>'
						print '<TR>'
						print '<TD ALIGN=CENTER NOWRAP><FONT FACE="Arial,Helvetica" SIZE="-1"><INPUT NAME="store" type="button" value=" Place Order " onClick="return execute(' + "'place_order'" + ')"></FONT></TD>'
						print '</TR></TABLE>'

						ecommerce.storeHiddenFields(form["uHidden"].value, form["pHidden"].value)
						ecommerce.retainAllHiddenFormFields(table_data,form)
						ecommerce.formToHiddenFields(table_data,'orders',form)

					else:

						# insert order into database
						table_data['orders']['subtotal']['value'] = '%10.2f' % (orderTotal)
						table_data['orders']['sales_tax']['value'] = '%9.2f' % (tax)
						table_data['orders']['shipping_handling']['value'] = '0.00'
						table_data['orders']['total']['value'] = '%9.2f' % (orderTotal + tax)
						table_data['orders']['order_status']['value'] = 'Pending Card Approval'
						
						if string.strip(table_data['customers']['email']['value']) != '':
							email_form = email_form + (80 * '-') + '\n'
							email_form = email_form + '\nOrder Summary:' + '\n\n'
							email_form = email_form + \
										 '          Sub total: ' + string.rjust(table_data['orders']['subtotal']['value'],int(table_data['orders']['subtotal']['form_size'])) + '\n' + \
										 '          Sales Tax: ' + string.rjust(table_data['orders']['sales_tax']['value'],int(table_data['orders']['sales_tax']['form_size'])) + '\n' + \
										 '  Shipping/Handling: ' + string.rjust(table_data['orders']['shipping_handling']['value'],int(table_data['orders']['shipping_handling']['form_size'])) + '\n' + \
										 '              Total: ' + string.rjust(table_data['orders']['total']['value'],int(table_data['orders']['total']['form_size'])) + '\n'
							email_form = email_form + (80 * '-') + '\n'

							# START FSBOW UNIQUE PROCESSING
							if properties_to_insert > 0:
								email_form = email_form + '\nYou have purchased 1 or more property ads.  You may enter the property data for your ad(s)\nonce your order has been approved by selecting the link below and depressing the [Query] button:\nhttp://%s/%s-cgi-bin/customer_property_admin.pyc?customer_id=%s&username=%s&password=%s' % (declarations.store_info['domain_name'],declarations.store_info['db_name'],table_data['customers']['id']['value'],table_data['customers']['account_username']['value'],table_data['customers']['account_password']['value'])

								email_form = email_form + '\n'
								email_form = email_form + 'If no property ads are listed then your order has not been approved yet.'
								email_form = email_form + '\n\n'
								
							# END FSBO UNIQUE PROCESSING
							
							email_form = email_form + '\nClickTree (Your on-line shopping network)\n'



						# send e-mail to customer about order
						if string.strip(table_data['customers']['email']['value']) != '':
							ecommerce.send_email('www.linuxden.com','sales@clicktree.com',[table_data['customers']['email']['value']],'Your order has been received!',email_form)
							
						# save the form from the table_data for customers
						dbResult = ecommerce.saveForm(table_data, db, table_data['orders']['id']['value'], "orders", " WHERE id = '" + table_data['orders']['id']['value'] + "'", form, 0, 0)
						
						# if the form was not successfully saved
						if dbResult['status'] != 'success':
							ecommerce.alertsArea(form,"Order data could not be saved due to an error during save,\n" + dbResult['message'] )


						# START UNIQUE PROCESSING
						# This BLOCK from START to END is specific to FSBO processing 
						for i in xrange(0,properties_to_insert):

							# create a new blank property for any ads ordered
							queryResult = ecommerce.executeSQL(db, "SELECT NEXTVAL('properties_id_seq')")
							
							dbResult = ecommerce.executeSQL(db, "INSERT INTO properties (id, customer_id, order_id, market_status) VALUES ('%d', '%s', '%s', '%s')" % (queryResult['result'][0]['nextval'],table_data['customers']['id']['value'],table_data['orders']['id']['value'],'For Sale'))
							
							# if the form was not successfully saved
							if dbResult['status'] != 'success':
								ecommerce.alertsArea(form,"Property data could not be inserted due to an error during save,\n" + dbResult['message'] )
							# END UNIQUE PROCESSING

						if string.strip(table_data['customers']['email']['value']) != '':
							ecommerce.printText('<BR><CENTER><B>You will receive an e-mail confirming your order.</B></CENTER>')
							ecommerce.printText('<CENTER><B>You may also want to print this page for your records.</B></CENTER>')
						else:
							ecommerce.printText('<BR><CENTER><B>Since you did not provide us with an e-mail address,</B></CENTER>')

							ecommerce.printText('<CENTER><B>please print this page for your records.</B></CENTER>')

						ecommerce.printText('<BR><CENTER><B>Thank you for your order!</B></CENTER>')
						

		print "</FORM>"

		ecommerce.trailer(table_data, db)
		db.close()

		print "</BODY>"
		print "</HTML>"

else:
	product_listing(None)
