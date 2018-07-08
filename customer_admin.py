# $Id: customer_admin.py,v 1.7 2000/04/06 00:43:49 davis Exp davis $
# Copyright (C) 1999 LinuXden, All Rights Reserved
# Copright Statement at http://www.linuxden.com/commerce.html
# Author: R. Scott Davis
# e-mail: rsdavis@linuxden.com
# 
import os, string, sys
import cgi, glob
from pg import DB
import declarations
import ecommerce

ecommerce.htmlContentType()

def query_customers(performDbQuery=0, onLoad=None, queryFields=None):

	table_data = declarations.define_tables()

	print "<HTML>"
	print "<HEAD>"

	ecommerce.javaScript("customer_admin", 1)

	ecommerce.title("Customer Administration")

	print "</HEAD>"

	ecommerce.bodySetup(onLoad)

	print '<CENTER>'
	print '<TABLE COLS=1 WIDTH=585>'
	print '<TR><TD>'

	ecommerce.mainHeading('Customer Administration')

	ecommerce.subHeading('Customer Listing')

	ecommerce.formSetup("customer_admin","customer_admin","return submitForm(document.customer_admin)",declarations.store_info['db_name'])

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

		dbResult = ecommerce.connectDB(
			username, 
			password, 
			declarations.store_info['db_name'])
		
		# could not connect to db
		if dbResult['status'] != 'success':
			
			ecommerce.alertsArea(form, "Can not connect to database,\n" + dbResult['message'])
			
			# connected to db

			ecommerce.queryFunctionButtons(0, declarations.store_info['help_file'])

		else:
			db = dbResult['result']
			
			queryFields, whereFields = ecommerce.getQueryWhereFields(form, table_data, 'customers')

			if queryFields == None or queryFields == []:
				queryFields = []
				whereFields = None
				queryFields.append('id')
				queryFields.append('first_name')
				queryFields.append('last_name')
				queryFields.append('street_1')
				queryFields.append('city')
				queryFields.append('state')

			dbResult, queryStatement = ecommerce.executeQuery(db, table_data, 'customers', queryFields, whereFields, 'query', ecommerce.queryItemFunctionsHtml)

			# if query was not successful
			if dbResult['status'] != 'success':
				ecommerce.alertsArea(form, "Could not retrieve customers from database,\n" + dbResult['message']);
			# else customers were retrieved ok
			else:
				ecommerce.alertsArea(form, "Last Query Statement: " + queryStatement + "\n" + `len(dbResult['result'])` + " customers retrieved from database");
				
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

		ecommerce.generate_form_javascript(table_data,'customers','customer_admin',0,0)

		ecommerce.title("Customer Administration")
		
		print "</HEAD>" 

		ecommerce.bodySetup()

		ecommerce.mainHeading('Customer Administration')
		
		ecommerce.subHeading('Edit Customer')

		ecommerce.formSetup("customer_admin","customer_admin","return submitForm(document.customer_admin)",declarations.store_info['db_name'])

		dbResult = ecommerce.connectDB(form["uHidden"].value, form["pHidden"].value, declarations.store_info['db_name'])
		
		if dbResult['status'] != 'success':
			ecommerce.alertsArea(form, "Could not connect to the database\n" + dbResult['message']);

		else:
			db = dbResult['result']

			sqlStatement = ecommerce.selectAllColumnsSqlStatement(table_data,'customers',form["key_id"].value)

#			sqlStatement = "SELECT p.id, p.date_built, p.car_garage, p.town, p.subdivision, p.style, p.full_basement, p.bedrooms, p.baths, p.square_footage, p.price, p.description, p.image, p.directions, p.heating_air, p.number_rooms, p.electric_service, p.school_district, p.acreage FROM customers p WHERE p.id = '" + form["key_id"].value + "'"

			dbResult = ecommerce.executeSQL(db, sqlStatement)

			if dbResult['status'] != 'success':

				ecommerce.alertsArea(form, "Could not retrieve customer data to edit\n" + dbResult['message']);

			else:

				result = dbResult['result']

				table_data = ecommerce.dbToTableData(table_data, 'customers', result[0])

				ecommerce.display_form(table_data, 'customers', 1, 'useValues', 1, db)
				
				ecommerce.alertsArea(form, "Customer data retrieved successfully");

		ecommerce.editFunctionButtons(form["key_id"].value, '/' + declarations.store_info['db_name'] + '-cgi-bin/customer_admin.pyc?username=' + form["uHidden"].value + '&password=' + form["pHidden"].value + '&performDbQuery=1', declarations.store_info['help_file'])

		ecommerce.editHiddenFields(form["uHidden"].value, form["pHidden"].value)
		
		print "</FORM>"

		ecommerce.trailer(table_data, db)

		db.close()
		
		print "</BODY>"
		print "</HTML>"
		
	elif form["action"].value == "query":

		query_customers(1)

	elif form["action"].value == "delete":

		dbResult = ecommerce.connectDB(form["uHidden"].value, form["pHidden"].value, declarations.store_info['db_name'])
		
		if dbResult['status'] != 'success':
			onQueryLoad = 'displayWindow("Could not connect to the database")'

		else:

			db = dbResult['result']

			# select all orders associated with customer
			selectOrdersResult = ecommerce.executeSQL(db, "SELECT id from ORDERS where customer_id = '" + form['key_id'].value + "'")

			if selectOrdersResult['status'] != 'success':
				onQueryLoad = "return displayWindow('Could not get orders for customer')"
			else:
				selectedOrders = selectOrdersResult['result']

				# for all orders associated with customer
				for i in xrange(0,len(selectedOrders)):
					
					# delete order_items associated with this order
					orderItemsResult = ecommerce.executeSQL(db, "DELETE from order_items WHERE order_id = '" + selectedOrders[i]['id'] + "'")

					if orderItemsResult['status'] != 'success':
						onQueryLoad = "return displayWindow('Could not delete order_items for customer')"

					# delete order_items associated with this order
					propsResult = ecommerce.executeSQL(db, "DELETE FROM properties WHERE order_id = '" + selectedOrders[i]['id'] + "'")

					if propsResult['status'] != 'success':
						onQueryLoad = "return displayWindow('Could not delete order_items for customer')"

				# delete order associated with customer
				selectOrdersResult = ecommerce.executeSQL(db, "DELETE FROM orders WHERE customer_id = '" + form['key_id'].value + "'")
				
				if selectOrdersResult['status'] != 'success':
					onQueryLoad = "return displayWindow('Could not get orders for customer')"

			sqlStatement = "DELETE FROM customers WHERE id = '" + form["key_id"].value + "'"

			dbResult = ecommerce.executeSQL(db, sqlStatement)

			if dbResult['status'] != 'success':

				onQueryLoad = "return displayWindow('Could not delete customer')"

			else:

				onQueryLoad = "return displayWindow('Customer successfully deleted')"

			db.close()

			query_customers(1)

	elif form["action"].value == "save":

		table_data = declarations.define_tables()

		print "<HTML>"
		print "<HEAD>"

		ecommerce.generate_form_javascript(table_data,'customers','customer_admin',0,0)

		ecommerce.title("Customer Administration")

		print "</HEAD>" 

		ecommerce.bodySetup()

		ecommerce.mainHeading('Customer Administration')

		ecommerce.subHeading('Edit Customer')

		ecommerce.formSetup("customer_admin","customer_admin","return submitForm(document.customer_admin)",declarations.store_info['db_name'])

		dbResult = ecommerce.connectDB(form["uHidden"].value, form["pHidden"].value, declarations.store_info['db_name'])

		if dbResult['status'] != 'success':

			 ecommerce.alertsArea(form,"Customer data could not be saved, could not connect to db" + dbResult['message'])

		else:

			db = dbResult['result']

			if form["key_id"].value == 'create':

				queryResult = ecommerce.executeSQL(db, "SELECT NEXTVAL('customer_id_seq')")

				form["key_id"].value = `queryResult['result'][0]['nextval']`

			# save the Form
			dbResult = ecommerce.saveForm(table_data, db, form["key_id"].value, "customers", " WHERE id = '" + form["key_id"].value + "'", form)

			# if the form was not successfully saved
			if dbResult['status'] != 'success':
				ecommerce.alertsArea(form,"Customer data could not be saved due to an error during save,\n" + dbResult['message'] )

			# form was successfully saved
			else:

				table_data = declarations.define_tables()
				table_data = ecommerce.formToTableData(table_data,'customers', form, form["key_id"].value)

				ecommerce.display_form(table_data, 'customers', 1, 'useValues', 1, db)
			
				ecommerce.alertsArea(form,"Customer data successfully saved")


		# generate function button row
		ecommerce.editFunctionButtons(form["key_id"].value, '/' + declarations.store_info['db_name'] + '-cgi-bin/customer_admin.pyc?username=' + form["uHidden"].value + '&password=' + form["pHidden"].value + '&performDbQuery=1', declarations.store_info['help_file'])
			
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

		ecommerce.generate_form_javascript(table_data,'customers','customer_admin',0,0)
		
		ecommerce.title("Create Customer")

		print "</HEAD>" 

		ecommerce.bodySetup()

		ecommerce.mainHeading('Customer Administration')

		ecommerce.subHeading('Create Customer')

		ecommerce.formSetup("customer_admin","customer_admin","return submitForm(document.customer_admin)",declarations.store_info['db_name'])

		# initialize form data values to zero or blank
		table_data = ecommerce.init_table_data(table_data, 'customers')

		# attempt to connect to db
		dbResult = ecommerce.connectDB(form["uHidden"].value,form["pHidden"].value, declarations.store_info['db_name'])
		
		# if db connection failed
		if dbResult['status'] != 'success':

			# generate appropriate message in alerts area
			 ecommerce.alertsArea(form,"Customer data could not be created, could not connect to db,\n" + dbResult['message'])			

		# else db connection succeeded
		else:

			# assign db connection variable
			db = dbResult['result']

			ecommerce.display_form(table_data, 'customers', 1,'useValues',1,db)
				
		# display alerts area to create
		ecommerce.alertsArea(form,"Enter information on form and depress Create button")

		# create functions button row
		ecommerce.createFunctionButtons('create', '/' + declarations.store_info['db_name'] + '-cgi-bin/customer_admin.pyc?username=' + form["uHidden"].value + '&password=' + form["pHidden"].value + '&performDbQuery=1', declarations.store_info['help_file'])

		# create hidden fields for form
		ecommerce.createHiddenFields(form["uHidden"].value, form["pHidden"].value)

		print "</FORM>"

		ecommerce.trailer(table_data, db)

		print "</BODY>"
		print "</HTML>"

	# view button pressed
	elif form["action"].value == "view":

		table_data = declarations.define_tables()

		print "<HTML>"
		print "<HEAD>"

		ecommerce.generate_form_javascript(table_data,'customers','customer_admin',0,0)

		ecommerce.title("View Customer Listing Code " + form['key_id'].value)

		print "</HEAD>" 

		ecommerce.bodySetup()

		ecommerce.mainHeading('Customer Administration')
	
		ecommerce.subHeading('View Customer')

		ecommerce.formSetup("customer_admin","customer_admin","return submitForm(document.customer_admin)",declarations.store_info['db_name'])

		# attempt to connect to db
		dbResult = ecommerce.connectDB(form["uHidden"].value,form["pHidden"].value, declarations.store_info['db_name'])
		
		# if db connection failed
		if dbResult['status'] != 'success':

			# generate appropriate message in alerts area
			 ecommerce.alertsArea(form,"Customer data could not be viewed, could not connect to db,\n" + dbResult['message'])			

		# else db connection succeeded
		else:

			# assign db connection variable
			db = dbResult['result']

			sqlStatement = ecommerce.selectAllColumnsSqlStatement(table_data,'customers',form["key_id"].value)

#			sqlStatement = "SELECT p.id, p.date_built, p.car_garage, p.town, p.subdivision, p.style, p.full_basement, p.bedrooms, p.baths, p.square_footage, p.price, p.description, p.image, p.directions, p.heating_air, p.number_rooms, p.electric_service, p.school_district, p.acreage FROM customers p WHERE p.id = '" + form["key_id"].value + "'"

			# execute select to retrieve customer ad data
			dbResult = ecommerce.executeSQL(db, sqlStatement)

			# if select failed
			if dbResult['status'] != 'success':
				
				# generate error in alerts area
				ecommerce.alertsArea(form,"Customer data could not be retrieved,\n" + dbResult['message'])

			# else select succeeded
			else:
				# assign result data
				result = dbResult['result']

				table_data = ecommerce.dbToTableData(table_data, 'customers', result[0])

				ecommerce.display_form(table_data, 'customers', 0)

		ecommerce.viewFunctionButtons('/'  + declarations.store_info['db_name'] + '-cgi-bin/customer_admin.pyc?username=' + form["uHidden"].value + '&password=' + form["pHidden"].value + '&performDbQuery=1', declarations.store_info['help_file'])

		print '</FORM>'

		ecommerce.trailer(table_data, db)

		db.close()

		print "</BODY>"
		print "</HTML>"

else:

	query_customers(0)
