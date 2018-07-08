# $Id: order_admin.py,v 1.7 2000/04/06 00:43:49 davis Exp davis $
# Copyright (C) 1999 LinuXden, All Rights Reserved
# Copright Statement at http://www.linuxden.com/copyrighted_apps.html
# 
import os, string, sys
import cgi, glob
from pg import DB
import ecommerce
import time_pkg
import declarations

ecommerce.htmlContentType()

def query_orders(performDbQuery=0, onLoad=None, queryFields=None):

	table_data = declarations.define_tables()

	print "<HTML>"
	print "<HEAD>"

	ecommerce.javaScript("order_admin", 1)

	ecommerce.title("Order Administration")

	print "</HEAD>"

	ecommerce.bodySetup(onLoad)

	print '<CENTER>'
	print '<TABLE COLS=1 WIDTH=585>'
	print '<TR><TD>'

	ecommerce.mainHeading('Order Administration')

	ecommerce.subHeading('Order Listing')

	ecommerce.formSetup("order_admin","order_admin","return submitForm(document.order_admin)",declarations.store_info['db_name'])

	if form.has_key("username"):
		username = form["username"].value
	else:
		if form.has_key("uHidden"):
			username = form["uHidden"].value
		else:
			username = ''

	if form.has_key("password"):
		password = form["password"].value
	else:
		if form.has_key("pHidden"):
			password = form["pHidden"].value
		else:
			password = ''

	ecommerce.usernamePasswordDisplay(username, password)

	if form.has_key("performDbQuery") or performDbQuery == 1:

		dbResult = ecommerce.connectDB(username, password, declarations.store_info['db_name'])
		
		# could not connect to db
		if dbResult['status'] != 'success':
			
			ecommerce.alertsArea(form, "Can not connect to database,\n" + dbResult['message'])
			
			# connected to db

			ecommerce.queryFunctionButtons(0, declarations.store_info['help_file'])

		else:

			db = dbResult['result']
			
			# check to see if a query has been performed with at least one column

			queryFields, whereFields = ecommerce.getQueryWhereFields(form, table_data, 'orders')

			if queryFields == None or queryFields == []:
				queryFields = []
				whereFields = None
				queryFields.append('id')
				queryFields.append('customer_id')
				queryFields.append('creation_date')
				queryFields.append('shipped_date')
				queryFields.append('total')

			dbResult, queryStatement = ecommerce.executeQuery(db, table_data, 'orders', queryFields, whereFields, 'query', ecommerce.queryItemFunctionsHtml)

			# if query was not successful
			if dbResult['status'] != 'success':
				ecommerce.alertsArea(form, "Invalid query where clause specified,\n" + dbResult['message'] + '\nLast Query Statement: ' +  queryStatement)

			# else orders were retrieved ok
			else:
				ecommerce.alertsArea(form, "Last Query Statement: " + queryStatement + "\n" + `len(dbResult['result'])` + " orders retrieved from database")
				
			ecommerce.queryFunctionButtons(1, declarations.store_info['help_file'])

	else:
		ecommerce.queryFunctionButtons(0, declarations.store_info['help_file'])

	ecommerce.queryHiddenFields(username, password)

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

	if form.has_key("performDbQuery") or performDbQuery == 1:
		return dbResult
	else:
		return {'status' : 'success', 'message' : 'query successful', 'result' : 0}

form = ecommerce.getFormData()

if form.has_key("action"):

	if form["action"].value == "edit":

		table_data = declarations.define_tables()

		print "<HTML>"
		print "<HEAD>"

		dbResult = ecommerce.connectDB(form["uHidden"].value, form["pHidden"].value,declarations.store_info['db_name'])
		
		if dbResult['status'] != 'success':
			ecommerce.alertsArea(form, "Could not connect to the database\n" + dbResult['message'])

		else:

			db = dbResult['result']

			dbResult = ecommerce.executeSQL(db, "SELECT line_item, order_id, product_id, quantity, quantity_shipped, price, line_subtotal FROM order_items WHERE order_id = '" + form['key_id'].value + "'")

			if dbResult['status'] != 'success':
			
				ecommerce.alertsArea(form, "Could not retrieve order data to edit\n" + dbResult['message'])
				print "</FORM>"
				
				ecommerce.trailer(table_data, db)
				db.close()

				print "</BODY>"
				print "</HTML>"
				sys.exit(1)
				
			result = dbResult['result']

			for i in xrange(0,len(result)):
				# add new items to table_data for validation only the
				# table data will be restored to db items after call

				table_data['orders']['quantity' + `i`] = { \
					'label' : 'Quantity', \
					'type' : 'INT4', \
					'db_size' : '4', \
					'form_size' : '3', \
					'default' : '0', \
					'display' : 'editable', \
					'value' : '', \
					'display_order' : 1, \
					'validation_routine' : 'valid_integer', \
					'validation_arguments' : ['form.quantity' + `i`,"''","'Quantity Item " + `i+1` + "'","true"], \
					'leaveFocus' : "checkBlankField(this, 'Quantity Item')", \
					'gainFocus' : "displayHint('Enter the quantity')", \
					'format' : "###" \
					}

				table_data['orders']['quantity_shipped' + `i`] = { \
					'label' : 'Shipped', \
					'type' : 'INT4', \
					'db_size' : '4', \
					'form_size' : '3', \
					'default' : '0', \
					'display' : 'editable', \
					'value' : '', \
					'display_order' : 1, \
					'validation_routine' : 'valid_integer', \
					'validation_arguments' : ['form.quantity_shipped' + `i`,"''","'Shipped Item " + `i+1` + "'","true"], \
					'leaveFocus' : "checkBlankField(this, 'Shipped Item')", \
					'gainFocus' : "displayHint('Enter the quantity shipped')", \
					'format' : "###" \
					}

				table_data['orders']['price' + `i`] = { \
					'label' : 'Price', \
					'type' : 'DECIMAL', \
					'db_size' : '9,2', \
					'form_size' : '10', \
					'default' : '0.00', \
					'display' : 'editable', \
					'value' : '', \
					'display_order' : 2, \
					'validation_routine' : 'valid_float', \
					'validation_arguments' : ['form.price' + `i`,"''","'Price Item " + `i+1` + "'","true"], \
					'leaveFocus' : "checkBlankField(this, 'Price')", \
					'gainFocus' : "displayHint('Enter the price of product')", \
					'format' : "#######.##" \
					}
				
			table_data['orders']['add_product_id'] = { \
				'label' : 'Add Product Id', \
				'type' : 'VARCHAR', \
				'db_size' : '10', \
				'form_size' : '10', \
				'default' : None, \
				'display' : 'editable', \
				'value' : '', \
				'display_order' : 1, \
				'validation_routine' : 'valid_integer', \
				'validation_arguments' : ['form.add_product_id',"''","'Product Id'","false"], \
				'leaveFocus' : "checkBlankField(this, 'Product Id')", \
				'gainFocus' : "displayHint('Enter the product id to add')" \
				}

			table_data['orders']['add_quantity'] = { \
				'label' : 'Add Quantity', \
				'type' : 'INT4', \
				'db_size' : '4', \
				'form_size' : '3', \
				'default' : '0', \
				'display' : 'editable', \
				'value' : '', \
				'display_order' : 2, \
				'validation_routine' : 'valid_integer', \
				'validation_arguments' : ['form.add_quantity',"''","'Quantity to Add'","false"], \
				'leaveFocus' : "checkBlankField(this, 'Quantity')", \
				'gainFocus' : "displayHint('Enter the quantity of product to add')", \
				'format' : "####" \
				}

			ecommerce.generate_form_javascript(table_data,'orders','order_admin',0)

			table_data = declarations.define_tables()
			
			ecommerce.title("Order Administration")
				
			print "</HEAD>" 
				
			ecommerce.bodySetup()
				
			ecommerce.mainHeading('Order Administration')
				
			ecommerce.subHeading('Edit Order')
				
			ecommerce.formSetup("order_admin","order_admin","return submitForm(document.order_admin)",declarations.store_info['db_name'])
				
			sqlStatement = ecommerce.selectAllColumnsSqlStatement(table_data,'orders',form["key_id"].value)

			dbResult = ecommerce.executeSQL(db, sqlStatement)

			if dbResult['status'] != 'success':

				ecommerce.alertsArea(form, "Could not retrieve order data to edit\n" + dbResult['message'])

			else:

				result = dbResult['result']

				table_data = ecommerce.dbToTableData(table_data, 'orders', result[0])

				ecommerce.display_form(table_data, 'orders', 1, 'useValues', 1, db)

				dbResult = ecommerce.executeSQL(db, "SELECT line_item, order_id, product_id, quantity, quantity_shipped, price, line_subtotal FROM order_items WHERE order_id = '" + form['key_id'].value + "'")

				if dbResult['status'] != 'success':

					ecommerce.alertsArea(form, "Could not retrieve order data to edit\n" + dbResult['message'])

				else:

					print '<HR>'
					ecommerce.printText('Items In Order')
					print '<TABLE BORDER=1>'
					print '<TR><TH>Line Item</TH><TH>Code</TH><TH>Quantity</TH><TH>Shipped</TH><TH>Description</TH><TH>Price</TH><TH>Extension</TH><TH>Message</TH><TH>Functions</TH></TR>'

					result = dbResult['result']

					if len(result) == 0:
						print '<TR><TD ALIGN=CENTER COLSPAN=7>No items in order</TD></TR>'

					for i in xrange(0,len(result)):
						print '<TR>'
						print '<TD ALIGN=CENTER>'
						ecommerce.printText(result[i]['line_item'],'black')
						print '</TD>'
						print '<TD ALIGN=CENTER>'

						ecommerce.printText(result[i]['product_id'])

						ecommerce.textbox('order_items','product_id' + `i`,result[i]['product_id'],table_data['order_items']['product_id']['form_size'],table_data['order_items']['product_id']['form_size'],None,None,'hidden')

						print '</TD>'

						print '<TD ALIGN=CENTER>'
						ecommerce.textbox('order_items','quantity' + `i`,`result[i]['quantity']`,table_data['order_items']['quantity']['form_size'],table_data['order_items']['quantity']['form_size'],None,None)
						print '</TD>'

						print '<TD ALIGN=CENTER>'
						ecommerce.textbox('order_items','quantity_shipped' + `i`,`result[i]['quantity_shipped']`,table_data['order_items']['quantity_shipped']['form_size'],table_data['order_items']['quantity_shipped']['form_size'],None,None)
						print '</TD>'

						priceResultQ = ecommerce.executeSQL(db, "SELECT description, price FROM products WHERE id = '" +  result[i]['product_id'] + "'")

						if priceResultQ['status'] != 'success':
							ecommerce.alertsArea(form,"Could not get price for order item,\n" + priceResultQ['message'] )
							print "</FORM>"
							
							ecommerce.trailer(table_data, db)
							db.close()

							print "</BODY>"
							print "</HTML>"
							sys.exit(1)

						priceResult = priceResultQ['result']

						print '<TD ALIGN=CENTER>'
						print priceResult[0]['description']
						print '</TD>'

						print '<TD ALIGN=CENTER>'
						ecommerce.textbox('order_items','price' + `i`,result[i]['price'],table_data['order_items']['price']['form_size'],table_data['order_items']['price']['form_size'],None,None)
						print '</TD>'
						print '<TD ALIGN=CENTER>'
						print result[i]['line_subtotal']

						print '</TD>'

						print '<TD ALIGN=CENTER>'
							
						if string.strip(result[i]['price']) != priceResult[0]['price']:
							print 'Price Override'

						print '</TD>'
						print '<TD ALIGN=CENTER>'
						print '<INPUT NAME="delete_item" type="button" value=" Delete " onClick="return process_item(' + "'delete_item'" + ", '" + result[i]['line_item'] + "', '" + form['key_id'].value + "'" + ')">'
						print '</TD>'
						print '</TR>'

					print '</TABLE>'


					print '<HR>'
					ecommerce.printText('Add Additional Item')
					print '<TABLE BORDER=1>'
					print '<TR><TH>Code</TH><TH>Quantity</TH></TR>'
					print '<TR>'

					print '<TD ALIGN=CENTER>'
					ecommerce.textbox('order_items','add_product_id','',table_data['order_items']['product_id']['form_size'],table_data['order_items']['product_id']['form_size'],None,None)
					print '</TD>'
					print '<TD ALIGN=CENTER>'
					ecommerce.textbox('order_items','add_quantity','',table_data['order_items']['quantity']['form_size'],table_data['order_items']['quantity']['form_size'],None,None)
					print '</TD>'
					print '</TR>'
					print '</TABLE>'
					print '<HR>'

				ecommerce.alertsArea(form, "Order data retrieved successfully")

		ecommerce.editFunctionButtons(form["key_id"].value, '/' + declarations.store_info['db_name'] + '-cgi-bin/order_admin.pyc?username=' + form["uHidden"].value + '&password=' + form["pHidden"].value + '&performDbQuery=1', declarations.store_info['help_file'])

		ecommerce.editHiddenFields(form["uHidden"].value, form["pHidden"].value, form['key_id'].value)
		
		print "</FORM>"

		ecommerce.trailer(table_data, db)

		# close db
		db.close()

		print "</BODY>"
		print "</HTML>"
		
	elif form["action"].value == "query":

		query_orders(1)

	elif form["action"].value == "delete":

		dbResult = ecommerce.connectDB(form["uHidden"].value, form["pHidden"].value,declarations.store_info['db_name'])
		
		if dbResult['status'] != 'success':
			onQueryLoad = 'displayWindow("Could not connect to the database")'

		else:
			db = dbResult['result']

			sqlStatement = "DELETE FROM properties WHERE order_id = '" + form["key_id"].value + "'"

			dbResult = ecommerce.executeSQL(db, sqlStatement)

			if dbResult['status'] != 'success':

				onQueryLoad = "return displayWindow('Could not delete property items')"

			else:

				onQueryLoad = "return displayWindow('Property items successfully deleted')"

			sqlStatement = "DELETE FROM order_items WHERE order_id = '" + form["key_id"].value + "'"

			dbResult = ecommerce.executeSQL(db, sqlStatement)

			if dbResult['status'] != 'success':

				onQueryLoad = "return displayWindow('Could not delete order items')"

			else:

				onQueryLoad = "return displayWindow('Order items successfully deleted')"


			sqlStatement = "DELETE FROM orders WHERE id = '" + form["key_id"].value + "'"

			dbResult = ecommerce.executeSQL(db, sqlStatement)

			if dbResult['status'] != 'success':

				onQueryLoad = "return displayWindow('Could not delete order')"

			else:

				onQueryLoad = "return displayWindow('Order successfully deleted')"

			db.close()

			query_orders(1)

	elif form["action"].value == "save" or form['action'].value == 'delete_item':

		table_data = declarations.define_tables()

		print "<HTML>"
		print "<HEAD>"

		dbResult = ecommerce.connectDB(form["uHidden"].value, form["pHidden"].value, declarations.store_info['db_name'])

		if dbResult['status'] != 'success':

			 ecommerce.alertsArea(form,"Order data could not be saved, could not connect to db" + dbResult['message'])

		else:

			db = dbResult['result']
			
			num_items = 0
			
			while 1:
				if not form.has_key('product_id' + `num_items`):
					break
				else:
					num_items = num_items + 1

			i = 0
			delete_performed = 0
			cur_line_item = 0

			while i < num_items:

				# add new items to table_data for validation only the
				# table data will be restored to db items after call
				
				if form['action'].value == 'delete_item' and not delete_performed:
					# if the order item line number = the item to delete
					if int(form['item_no'].value) == (i + 1):
						delete_performed = 1
						i = i + 1
						continue

				table_data['orders']['quantity' + `cur_line_item`] = { \
					'label' : 'Quantity', \
					'type' : 'INT4', \
					'db_size' : '4', \
					'form_size' : '3', \
					'default' : '0', \
					'display' : 'editable', \
					'value' : '', \
					'display_order' : 1, \
					'validation_routine' : 'valid_integer', \
					'validation_arguments' : ['form.quantity' + `cur_line_item`,"''","'Quantity Item " + `cur_line_item+1` + "'","true"], \
					'leaveFocus' : "checkBlankField(this, 'Quantity Item')", \
					'gainFocus' : "displayHint('Enter the quantity')", \
					'format' : "###" \
					}

				table_data['orders']['quantity_shipped' + `cur_line_item`] = { \
					'label' : 'Shipped', \
					'type' : 'INT4', \
					'db_size' : '4', \
					'form_size' : '3', \
					'default' : '0', \
					'display' : 'editable', \
					'value' : '', \
					'display_order' : 1, \
					'validation_routine' : 'valid_integer', \
					'validation_arguments' : ['form.quantity_shipped' + `cur_line_item`,"''","'Shipped Item " + `cur_line_item+1` + "'","true"], \
					'leaveFocus' : "checkBlankField(this, 'Shipped Item')", \
					'gainFocus' : "displayHint('Enter the quantity shipped')", \
					'format' : "###" \
					}

				table_data['orders']['price' + `cur_line_item`] = { \
					'label' : 'Price', \
					'type' : 'DECIMAL', \
					'db_size' : '9,2', \
					'form_size' : '10', \
					'default' : '0.00', \
					'display' : 'editable', \
					'value' : '', \
					'display_order' : 2, \
					'validation_routine' : 'valid_float', \
					'validation_arguments' : ['form.price' + `cur_line_item`,"''","'Price Item " + `cur_line_item+1` + "'","true"], \
					'leaveFocus' : "checkBlankField(this, 'Price')", \
					'gainFocus' : "displayHint('Enter the price of product')", \
					'format' : "#######.##" \
					}

				i = i + 1
				cur_line_item = cur_line_item + 1

			if string.strip(form['add_product_id'].value) != '' and \
			   string.strip(form['add_quantity'].value) != '':
				
				table_data['orders']['quantity' + `cur_line_item`] = { \
					'label' : 'Quantity', \
					'type' : 'INT4', \
					'db_size' : '4', \
					'form_size' : '3', \
					'default' : '0', \
					'display' : 'editable', \
					'value' : '', \
					'display_order' : 1, \
					'validation_routine' : 'valid_integer', \
					'validation_arguments' : ['form.quantity' + `cur_line_item`,"''","'Quantity Item " + `cur_line_item+1` + "'","true"], \
					'leaveFocus' : "checkBlankField(this, 'Quantity Item')", \
					'gainFocus' : "displayHint('Enter the quantity')", \
					'format' : "###" \
					}

				table_data['orders']['quantity_shipped' + `cur_line_item`] = { \
					'label' : 'Shipped', \
					'type' : 'INT4', \
					'db_size' : '4', \
					'form_size' : '3', \
					'default' : '0', \
					'display' : 'editable', \
					'value' : '', \
					'display_order' : 1, \
					'validation_routine' : 'valid_integer', \
					'validation_arguments' : ['form.quantity_shipped' + `cur_line_item`,"''","'Shipped Item " + `cur_line_item+1` + "'","true"], \
					'leaveFocus' : "checkBlankField(this, 'Shipped Item')", \
					'gainFocus' : "displayHint('Enter the quantity shipped')", \
					'format' : "###" \
					}

				table_data['orders']['price' + `cur_line_item`] = { \
					'label' : 'Price', \
					'type' : 'DECIMAL', \
					'db_size' : '9,2', \
					'form_size' : '10', \
					'default' : '0.00', \
					'display' : 'editable', \
					'value' : '', \
					'display_order' : 2, \
					'validation_routine' : 'valid_float', \
					'validation_arguments' : ['form.price' + `cur_line_item`,"''","'Price Item " + `cur_line_item+1` + "'","true"], \
					'leaveFocus' : "checkBlankField(this, 'Price')", \
					'gainFocus' : "displayHint('Enter the price of product')", \
					'format' : "#######.##" \
					}

			table_data['orders']['add_product_id'] = { \
				'label' : 'Add Product Id', \
				'type' : 'VARCHAR', \
				'db_size' : '10', \
				'form_size' : '10', \
				'default' : None, \
				'display' : 'editable', \
				'value' : '', \
				'display_order' : 1, \
				'validation_routine' : 'valid_integer', \
				'validation_arguments' : ['form.add_product_id',"''","'Product Id'","false"], \
				'leaveFocus' : "checkBlankField(this, 'Product Id')", \
				'gainFocus' : "displayHint('Enter the product id to add')" \
				}

			table_data['orders']['add_quantity'] = { \
				'label' : 'Add Quantity', \
				'type' : 'INT4', \
				'db_size' : '4', \
				'form_size' : '3', \
				'default' : '0', \
				'display' : 'editable', \
				'value' : '', \
				'display_order' : 2, \
				'validation_routine' : 'valid_integer', \
				'validation_arguments' : ['form.add_quantity',"''","'Quantity to Add'","false"], \
				'leaveFocus' : "checkBlankField(this, 'Quantity')", \
				'gainFocus' : "displayHint('Enter the quantity of product to add')", \
				'format' : "####" \
				}

			ecommerce.generate_form_javascript(table_data,'orders','order_admin',0,0)

			table_data = declarations.define_tables()
			
			ecommerce.title("Order Administration")
			
			print "</HEAD>" 
			
			ecommerce.bodySetup()
			
			ecommerce.mainHeading('Order Administration')
			
			ecommerce.subHeading('Edit Order')
			
			ecommerce.formSetup("order_admin","order_admin","return submitForm(document.order_admin)",declarations.store_info['db_name'])

			this_is_a_create = 0

			if form["key_id"].value == 'create':

				this_is_a_create = 1

				queryResult = ecommerce.executeSQL(db, "SELECT NEXTVAL('orders_id_seq')")

				form["key_id"].value = `queryResult['result'][0]['nextval']`

				ecommerce.formToTableData(table_data,'orders',form)

			if not this_is_a_create:

				ecommerce.formToTableData(table_data,'orders',form)

				# delete all order items currently in db
				sqlStatement = "DELETE FROM order_items WHERE order_id = '" + form["key_id"].value + "'"
				
				dbResult = ecommerce.executeSQL(db, sqlStatement)
				
				if dbResult['status'] != 'success':
					ecommerce.alertsArea(form,"Order items could not be deleted prior to insert,\n" + dbResult['message'] )
					print "</FORM>"
					
					ecommerce.trailer(table_data, db)
					db.close()

					print "</BODY>"
					print "</HTML>"
					sys.exit(1)

				updatePropertyAdsResult = ecommerce.executeSQL(
					db, 
					"SELECT count(*) FROM properties WHERE order_id = '" + form['key_id'].value + "'")
					
				if updatePropertyAdsResult['status'] != 'success':
					
					ecommerce.alertsArea(form, "Could not get count for order properties\n" + orderTotalResult['message'])
					
					print "</FORM>"

					ecommerce.trailer(table_data, db)
					db.close()

					print "</BODY>"
					print "</HTML>"
					sys.exit(1)

				result = updatePropertyAdsResult['result']
				
				if result[0]['count'] > 0:

					if form['order_status'].value == 'Order Approved' or \
					   form['order_status'].value[:13] == 'Order Shipped':
						display_status = 't'
					else:
						display_status = 'f'

					updatePropertyAdsResult = ecommerce.executeSQL(
						db, 
						"UPDATE properties SET display_property = '" + display_status + "' WHERE customer_id = '" + form['customer_id'].value + "' and order_id = '" + form['key_id'].value + "'")

					if updatePropertyAdsResult['status'] != 'success':

						ecommerce.alertsArea(form, "Could not update properties display ad field\n" + orderTotalResult['message'])
						
						print "</FORM>"
						
						ecommerce.trailer(table_data, db)
						db.close()

						print "</BODY>"
						print "</HTML>"
						sys.exit(1)

				num_items = 0
			
				while 1:
					if not form.has_key('product_id' + `num_items`):
						break
					else:
						num_items = num_items + 1

				i = 0
				cur_line_item = 1
				delete_performed = 0

				# loop through all order items on page
				while i < num_items:

					# if the form action is to delete an order item and the delete has not been performed
					if form['action'].value == 'delete_item' and not delete_performed:
						# if the order item line number = the item to delete
						if int(form['item_no'].value) == (i + 1):

							descripResultQ = ecommerce.executeSQL(
								db, 
								"SELECT description FROM products WHERE id = '" + string.strip(form['product_id' + `i`].value) + "'")
							
							if descripResultQ['status'] != 'success':
								ecommerce.alertsArea(form,"Could not get description for order item,\n" + descripResultQ['message'] )
								print "</FORM>"
								
								ecommerce.trailer(table_data, db)
								db.close()

								print "</BODY>"
								print "</HTML>"
								sys.exit(1)
								
							descripResult = descripResultQ['result']

							# if the description of product includes Ad then
							# the product being removed is a property ad so
							# remove the property ad
							if descripResult[0]['description'][-2:] == 'Ad':
								
								sqlStatement = "DELETE FROM properties WHERE order_id = '" + form["key_id"].value + "'"
								
								deletePropResult = ecommerce.executeSQL(db, sqlStatement)

								if deletePropResult['status'] != 'success':
									
									ecommerce.alertsArea(form,"Property ad could not be deleted due to an error,\n" + dbResult['message'] )
									print "</FORM>"
									
									ecommerce.trailer(table_data, db)
									db.close()

									print "</BODY>"
									print "</HTML>"
									sys.exit(1)
									
							# signify that the item has been skipped over
							delete_performed = 1
							# skip over item
							i = i + 1
							continue

					table_data['order_items']['line_item']['value'] = `cur_line_item`
				
					table_data['order_items']['order_id']['value'] = form['key_id'].value
					table_data['order_items']['product_id']['value'] = string.strip(form['product_id' + `i`].value)
					table_data['order_items']['quantity']['value'] = string.strip(form['quantity' + `i`].value)
					table_data['order_items']['quantity_shipped']['value'] = string.strip(form['quantity_shipped' + `i`].value)
					table_data['order_items']['price']['value'] = string.strip(form['price' + `i`].value)
				
					lineTotal = string.atoi(form['quantity' + `i`].value) * string.atof(form['price'+ `i`].value)
				
					table_data['order_items']['line_subtotal']['value'] = '%9.2f' % (lineTotal)
				
					# put order item in db
					dbResult = ecommerce.saveForm(table_data, db, None, "order_items", None, form, 0, 0, 1)

					# if the form was not successfully saved
					if dbResult['status'] != 'success':
						ecommerce.alertsArea(form,"Order items could not be saved due to an error during save,\n" + dbResult['message'] )
						print "</FORM>"
						
						ecommerce.trailer(table_data, db)
						db.close()

						print "</BODY>"
						print "</HTML>"
						sys.exit(1)

					i = i + 1
					cur_line_item = cur_line_item + 1

			else:
				num_items = 0

			# process new item
			if string.strip(form['add_product_id'].value) != '' and \
			   string.strip(form['add_quantity'].value) != '':
				
				table_data['order_items']['line_item']['value'] = `num_items+1`
				table_data['order_items']['order_id']['value'] = form['key_id'].value
				table_data['order_items']['product_id']['value'] = form['add_product_id'].value
				table_data['order_items']['quantity']['value'] = form['add_quantity'].value
				table_data['order_items']['quantity_shipped']['value'] = '0'

				priceResultQ = ecommerce.executeSQL(db, "SELECT price FROM products WHERE id = '" +  string.strip(form['add_product_id'].value) + "'")

				if priceResultQ['status'] != 'success':
					ecommerce.alertsArea(form,"Could not get price for order item added,\n" + priceResultQ['message'] )

					print "</FORM>"

					ecommerce.trailer(table_data, db)
					db.close()

					print "</BODY>"
					print "</HTML>"
					sys.exit(1)
					
				priceResult = priceResultQ['result']

				if len(priceResult) == 0:
					ecommerce.alertsArea(form,"Can not find specified product to add to order,\n" + priceResultQ['message'] )

					print "</FORM>"
					
					ecommerce.trailer(table_data, db)
					db.close()

					print "</BODY>"
					print "</HTML>"
					sys.exit(1)

				table_data['order_items']['price']['value'] = priceResult[0]['price']

				lineTotal = string.atoi(form['add_quantity'].value) * string.atof(priceResult[0]['price'])
				
				table_data['order_items']['line_subtotal']['value'] = '%9.2f' % (lineTotal)
				
				# put order item in db
				dbResult = ecommerce.saveForm(table_data, db, None, "order_items", None, form, 0, 0, 1)
								
				# if the form was not successfully saved
				if dbResult['status'] != 'success':
					ecommerce.alertsArea(form,"Order items could not be saved due to an error during save,\n" + dbResult['message'] )

					print "</FORM>"
					
					ecommerce.trailer(table_data, db)
					db.close()

					print "</BODY>"
					print "</HTML>"
					sys.exit(1)

			# calculate order total
			orderTotalResult = ecommerce.executeSQL(db, "SELECT line_subtotal FROM order_items WHERE order_id = '" + form['key_id'].value + "'")
				
			if orderTotalResult['status'] != 'success':

				ecommerce.alertsArea(form, "Could not retrieve order data to edit\n" + orderTotalResult['message'])

			else:
				
				subTotalsResult = orderTotalResult['result']
				
				order_subtotal = 0.0
				
				for i in xrange(0,len(subTotalsResult)):
					
					order_subtotal = order_subtotal + string.atof(subTotalsResult[i]['line_subtotal'])
					
				taxResultQ = ecommerce.executeSQL(db, "SELECT tax FROM sales_tax_by_state WHERE state_abbreviation = '" + string.upper(form['state'].value) + "'")
		
				if taxResultQ['status'] != 'success':
					
					ecommerce.alertsArea(form, "Could not charge tax based on state entered\n" + taxResultQ['message'])
					
				else:
					
					taxResult = taxResultQ['result']
					
					if taxResult != []:
						table_data = ecommerce.dbToTableData(table_data, 'sales_tax_by_state', taxResult[0])
					else:
						table_data = ecommerce.dbToTableData(table_data, 'sales_tax_by_state', {'tax' : 0.00})
						
					tax = float(table_data['sales_tax_by_state']['tax']['value']) * float(order_subtotal)

					table_data['orders']['id']['value'] = form['key_id'].value
					
					table_data['orders']['subtotal']['value'] = '%10.2f' % (order_subtotal)
					table_data['orders']['sales_tax']['value'] = '%9.2f' % (tax)
					
					table_data['orders']['total']['value'] = '%10.2f' % (float(table_data['orders']['subtotal']['value']) + float(table_data['orders']['sales_tax']['value']))
					
					# save the Form
					dbResult = ecommerce.saveForm(table_data, db, form['key_id'].value, "orders", " WHERE id = '" + form["key_id"].value + "'", form, 0, 0)
					
					# if the form was not successfully saved
					if dbResult['status'] != 'success':
						ecommerce.alertsArea(form,"Order data could not be saved due to an error during save,\n" + dbResult['message'] )
						print "</FORM>"
						
						ecommerce.trailer(table_data, db)
						db.close()

						print "</BODY>"
						print "</HTML>"
						sys.exit(1)
						
					queryResult = ecommerce.executeSQL(db, "COMMIT")
					
					ecommerce.display_form(table_data, 'orders', 1, 'useValues', 1, db)
					
					dbResult = ecommerce.executeSQL(db, "SELECT line_item, order_id, product_id, quantity, quantity_shipped, price, line_subtotal FROM order_items WHERE order_id = '" + form['key_id'].value + "'")

					if dbResult['status'] != 'success':
							
						ecommerce.alertsArea(form, "Could not retrieve order items to edit\n" + dbResult['message'])

					else:
						
						print '<HR>'
						ecommerce.printText('Items In Order')
						print '<TABLE BORDER=1>'
						print '<TR><TH>Line Item</TH><TH>Code</TH><TH>Quantity</TH><TH>Shipped</TH><TH>Description</TH><TH>Price</TH><TH>Extension</TH><TH>Message</TH><TH>Functions</TH></TR>'
						
						result = dbResult['result']
						
						if len(result) == 0:
							print '<TR><TD ALIGN=CENTER COLSPAN=7>No items in order</TD></TR>'

						for i in xrange(0,len(result)):
							print '<TR>'
							print '<TD ALIGN=CENTER>'
							ecommerce.printText(result[i]['line_item'],'black')
							print '</TD>'

							print '<TD ALIGN=CENTER>'
							ecommerce.printText(result[i]['product_id'])
							ecommerce.textbox('order_items','product_id' + `i`,result[i]['product_id'],table_data['order_items']['product_id']['form_size'],table_data['order_items']['product_id']['form_size'],None,None,'hidden')
							print '</TD>'

							print '<TD ALIGN=CENTER>'
							ecommerce.textbox('order_items','quantity' + `i`,`result[i]['quantity']`,table_data['order_items']['quantity']['form_size'],table_data['order_items']['quantity']['form_size'],None,None)
							print '</TD>'

							print '<TD ALIGN=CENTER>'
							ecommerce.textbox('order_items','quantity_shipped' + `i`,`result[i]['quantity_shipped']`,table_data['order_items']['quantity_shipped']['form_size'],table_data['order_items']['quantity_shipped']['form_size'],None,None)
							print '</TD>'

							priceResultQ = ecommerce.executeSQL(db, "SELECT description, price FROM products WHERE id = '" +  result[i]['product_id'] + "'")
							
							if priceResultQ['status'] != 'success':
								ecommerce.alertsArea(form,"Could not get price for order item,\n" + priceResultQ['message'] )
								print "</FORM>"
								
								ecommerce.trailer(table_data, db)
								db.close()

								print "</BODY>"
								print "</HTML>"
								sys.exit(1)
								
							priceResult = priceResultQ['result']

							print '<TD ALIGN=CENTER>'
							print priceResult[0]['description']
							print '</TD>'

							print '<TD ALIGN=CENTER>'
							ecommerce.textbox('order_items','price' + `i`,result[i]['price'],table_data['order_items']['price']['form_size'],table_data['order_items']['price']['form_size'],None,None)
							print '</TD>'
							print '<TD ALIGN=CENTER>'
							print result[i]['line_subtotal']
							#textbox('order_items','line_subtotal' + `i`,result[i]['line_subtotal'],table_data['order_items']['line_subtotal']['form_size'],table_data['order_items']['line_subtotal']['form_size'],None,None)
							print '</TD>'
							
							print '<TD ALIGN=CENTER>'
														
							if string.strip(result[i]['price']) != string.strip(priceResult[0]['price']):
								print 'Price Override'
								
							print '</TD>'

							print '<TD ALIGN=CENTER>'
							print '<INPUT NAME="delete_item" type="button" value=" Delete " onClick="return process_item(' + "'delete_item'" + ", '" + result[i]['line_item'] + "', '" + form['key_id'].value + "'" + ')">'
							print '</TD>'
							print '</TR>'
							
						print '</TABLE>'
							
						print '<HR>'

			ecommerce.printText('Add Additional Item')
			print '<TABLE BORDER=1>'
			print '<TR><TH>Code</TH><TH>Quantity</TH></TR>'
			print '<TR>'
			
			print '<TD ALIGN=CENTER>'
			ecommerce.textbox('order_items','add_product_id','',table_data['order_items']['product_id']['form_size'],table_data['order_items']['product_id']['form_size'],None,None)
			print '</TD>'
			print '<TD ALIGN=CENTER>'
			ecommerce.textbox('order_items','add_quantity','',table_data['order_items']['quantity']['form_size'],table_data['order_items']['quantity']['form_size'],None,None)
			print '</TD>'
			print '</TR>'
			print '</TABLE>'
			print '<HR>'

			ecommerce.alertsArea(form,"Order data successfully saved")
			
		# generate function button row
		ecommerce.editFunctionButtons(form["key_id"].value, '/' + declarations.store_info['db_name'] + '-cgi-bin/order_admin.pyc?username=' + form["uHidden"].value + '&password=' + form["pHidden"].value + '&performDbQuery=1', declarations.store_info['help_file'])
			
		# generate hidden fields for form
		ecommerce.createHiddenFields(form["uHidden"].value, form["pHidden"].value)
			
		print "</FORM>"
		
		ecommerce.trailer(table_data, db)

		# close db
		db.close()

		print "</BODY>"
		print "</HTML>"
			
	# create button was pressed on form
	elif form["action"].value == "create":

		print "<HTML>"
		print "<HEAD>"

		table_data = declarations.define_tables()

		table_data['orders']['add_product_id'] = { \
			'label' : 'Add Product Id', \
			'type' : 'VARCHAR', \
			'db_size' : '10', \
			'form_size' : '10', \
			'default' : None, \
			'display' : 'editable', \
			'value' : '', \
			'display_order' : 1, \
			'validation_routine' : 'valid_integer', \
			'validation_arguments' : ['form.add_product_id',"''","'Product Id'","false"], \
			'leaveFocus' : "checkBlankField(this, 'Product Id')", \
			'gainFocus' : "displayHint('Enter the product id to add')" \
			}
		
		table_data['orders']['add_quantity'] = { \
			'label' : 'Add Quantity', \
			'type' : 'INT4', \
			'db_size' : '4', \
			'form_size' : '3', \
			'default' : '0', \
				'display' : 'editable', \
			'value' : '', \
			'display_order' : 2, \
			'validation_routine' : 'valid_integer', \
			'validation_arguments' : ['form.add_quantity',"''","'Quantity to Add'","false"], \
			'leaveFocus' : "checkBlankField(this, 'Quantity')", \
			'gainFocus' : "displayHint('Enter the quantity of product to add')", \
			'format' : "####" \
			}

		ecommerce.generate_form_javascript(table_data,'orders','order_admin',0,0)

		table_data = declarations.define_tables()
		
		ecommerce.title("Create Order")

		print "</HEAD>" 

		ecommerce.bodySetup()

		ecommerce.mainHeading('Order Administration')

		ecommerce.subHeading('Create Order')

		ecommerce.formSetup("order_admin","order_admin","return submitForm(document.order_admin)",declarations.store_info['db_name'])

		# initialize form data values to zero or blank
		table_data = declarations.init_table_data(table_data,'orders')

		# attempt to connect to db
		dbResult = ecommerce.connectDB(form["uHidden"].value,form["pHidden"].value,declarations.store_info['db_name'])
		
		# if db connection failed
		if dbResult['status'] != 'success':

			# generate appropriate message in alerts area
			 ecommerce.alertsArea(form,"Customer data could not be created, could not connect to db,\n" + dbResult['message'])			

		# else db connection succeeded
		else:

			# assign db connection variable
			db = dbResult['result']

			table_data['orders']['creation_date']['value'] = time_pkg.current_time_MM_DD_YYYY()

			ecommerce.display_form(table_data, 'orders', 1, 'useValues', 1, db)

			print '<HR>'
			ecommerce.printText('Add Additional Item')
			print '<TABLE BORDER=1>'
			print '<TR><TH>Code</TH><TH>Quantity</TH></TR>'
			print '<TR>'
			
			print '<TD ALIGN=CENTER>'
			ecommerce.textbox('order_items','add_product_id','',table_data['order_items']['product_id']['form_size'],table_data['order_items']['product_id']['form_size'],None,None)
			print '</TD>'
			print '<TD ALIGN=CENTER>'
			ecommerce.textbox('order_items','add_quantity','',table_data['order_items']['quantity']['form_size'],table_data['order_items']['quantity']['form_size'],None,None)
			print '</TD>'
			print '</TR>'
			print '</TABLE>'
			print '<HR>'
				
		# display alerts area to create
		ecommerce.alertsArea(form,"Enter information on form and depress Create button")

		# create functions button row
		ecommerce.createFunctionButtons('create', '/' + declarations.store_info['db_name'] + '-cgi-bin/order_admin.pyc?username=' + form["uHidden"].value + '&password=' + form["pHidden"].value + '&performDbQuery=1', declarations.store_info['help_file'])

		# create hidden fields for form
		ecommerce.createHiddenFields(form["uHidden"].value, form["pHidden"].value)

		print "</FORM>"
		
		ecommerce.trailer(table_data, db)
		db.close()

		print "</BODY>"
		print "</HTML>"

	# view button pressed
	elif form["action"].value == "view":

		table_data = declarations.define_tables()

		print "<HTML>"
		print "<HEAD>"

		ecommerce.generate_form_javascript(table_data,'orders','order_admin',0,0)

		ecommerce.title("View Order Listing Code " + form['key_id'].value)

		print "</HEAD>" 

		ecommerce.bodySetup()

		ecommerce.mainHeading('Order Administration')
	
		ecommerce.subHeading('View Order')

		ecommerce.formSetup("order_admin","order_admin","return submitForm(document.order_admin)",declarations.store_info['db_name'])

		# attempt to connect to db
		dbResult = ecommerce.connectDB(form["uHidden"].value,form["pHidden"].value,declarations.store_info['db_name'])
		
		# if db connection failed
		if dbResult['status'] != 'success':

			# generate appropriate message in alerts area
			 ecommerce.alertsArea(form,"Order data could not be viewed, could not connect to db,\n" + dbResult['message'])			

		# else db connection succeeded
		else:

			# assign db connection variable
			db = dbResult['result']

			sqlStatement = ecommerce.selectAllColumnsSqlStatement(table_data,'orders',form["key_id"].value)

			# execute select to retrieve order ad data
			dbResult = ecommerce.executeSQL(db, sqlStatement)

			# if select failed
			if dbResult['status'] != 'success':
				
				# generate error in alerts area
				ecommerce.alertsArea(form,"Order data could not be retrieved,\n" + dbResult['message'])

			# else select succeeded
			else:
				# assign result data
				result = dbResult['result']

				table_data = ecommerce.dbToTableData(table_data, 'orders', result[0])

				ecommerce.display_form(table_data, 'orders', 0)

				dbResult = ecommerce.executeSQL(db, "SELECT line_item, order_id, product_id, quantity, quantity_shipped, price, line_subtotal FROM order_items WHERE order_id = '" + form['key_id'].value + "'")

				if dbResult['status'] != 'success':

					ecommerce.alertsArea(form, "Could not retrieve order items to edit\n" + dbResult['message'])

				else:

					print '<HR>'
					ecommerce.printText('Items In Order')
					print '<TABLE BORDER=1>'
					print '<TR><TH>Line Item</TH><TH>Code</TH><TH>Quantity</TH><TH>Shipped</TH><TH>Description</TH><TH>Price</TH><TH>Extension</TH><TH>Message</TH></TR>'

					result = dbResult['result']

					if len(result) == 0:
						print '<TR><TD ALIGN=CENTER COLSPAN=7>No items in order</TD></TR>'

					for i in xrange(0,len(result)):
						print '<TR>'
						print '<TD ALIGN=CENTER>'
						ecommerce.printText(result[i]['line_item'],'black')
						print '</TD>'
						print '<TD ALIGN=CENTER>'
						print result[i]['product_id']
						print '</TD>'
						print '<TD ALIGN=CENTER>'
						print `result[i]['quantity']`
						print '</TD>'
						print '<TD ALIGN=CENTER>'
						print `result[i]['quantity_shipped']`
						print '</TD>'

						priceResultQ = ecommerce.executeSQL(db, "SELECT description, price FROM products WHERE id = '" +  result[i]['product_id'] + "'")

						if priceResultQ['status'] != 'success':
							ecommerce.alertsArea(form,"Could not get price for order item,\n" + priceResultQ['message'] )
							print "</FORM>"
							
							ecommerce.trailer(table_data, db)
							db.close()

							print "</BODY>"
							print "</HTML>"
							sys.exit(1)
							
						priceResult = priceResultQ['result']

						print '<TD ALIGN=CENTER>'
						print priceResult[0]['description']
						print '</TD>'

						print '<TD ALIGN=CENTER>'
						print result[i]['price']
						print '</TD>'
						print '<TD ALIGN=CENTER>'
						print result[i]['line_subtotal']
						print '</TD>'

						print '<TD ALIGN=CENTER>'


						if string.strip(result[i]['price']) != string.strip(priceResult[0]['price']):
							print 'Price Override'

						print '</TD>'

						print '</TR>'

					print '</TABLE>'


		ecommerce.viewFunctionButtons('/' + declarations.store_info['db_name'] + '-cgi-bin/order_admin.pyc?username=' + form["uHidden"].value + '&password=' + form["pHidden"].value + '&performDbQuery=1', declarations.store_info['help_file'])

		print '</FORM>'

		ecommerce.trailer(table_data, db)

		db.close()

		print "</BODY>"
		print "</HTML>"

else:

	query_orders(0)
