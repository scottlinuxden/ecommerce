# $Id: sales_tax_admin.py,v 1.7 2000/04/06 00:38:25 davis Exp $
# Copyright (C) 1999 LinuXden, All Rights Reserved
# Copright Statement at http://www.linuxden.com/copyrighted_apps.html
# 
import os, string, sys
import cgi, glob
from pg import DB
import ecommerce
import declarations

ecommerce.htmlContentType()

def query_sales_tax(performDbQuery=0, onLoad=None, queryFields=None):

	table_data = declarations.define_tables()

	print "<HTML>"
	print "<HEAD>"

	ecommerce.javaScript("sales_tax_admin", 1)

	ecommerce.title("Sales Tax Administration")

	print "</HEAD>"

	ecommerce.bodySetup(onLoad)

	ecommerce.mainHeading('Sales Tax Administration')

	ecommerce.subHeading('Sales Tax by State')

	ecommerce.formSetup("sales_tax_admin","sales_tax_admin","return submitForm(document.sales_tax_admin)",declarations.store_info['db_name'])

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
			
			# execute query
			# dbResult = queryCustomers(db, 'query')

			# check to see if a query has been performed with at least one column

			queryFields, whereFields = ecommerce.getQueryWhereFields(form, table_data, 'sales_tax_by_state')

			if queryFields == None or queryFields == []:
				queryFields = []
				whereFields = None
				queryFields.append('state_name')
				queryFields.append('state_abbreviation')
				queryFields.append('tax')

			dbResult, queryStatement = ecommerce.executeQuery(db, table_data, 'sales_tax_by_state', queryFields, whereFields, 'query', ecommerce.queryItemFunctionsHtmlNoEdit, 'ORDER by state_abbreviation','state_abbreviation')

			# if query was not successful
			if dbResult['status'] != 'success':
				ecommerce.alertsArea(form, "Could not retrieve sales tax data from database,\n" + dbResult['message']);
			# else sales tax data was retrieved ok
			else:
				ecommerce.alertsArea(form, "Last Query Statement: " + queryStatement + "\n" + `len(dbResult['result'])` + " sales tax items retrieved from database");
				
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

		ecommerce.generate_form_javascript(table_data,'sales_tax_by_state','sales_tax_admin',0,0)

		ecommerce.title("Sales Tax Administration")
		
		print "</HEAD>" 

		ecommerce.bodySetup()

		ecommerce.mainHeading('Sales Tax Administration')
		
		ecommerce.subHeading('Edit Sales Tax Data')

		ecommerce.formSetup("sales_tax_admin","sales_tax_admin","return submitForm(document.sales_tax_admin)",declarations.store_info['db_name'])

		dbResult = ecommerce.connectDB(form["uHidden"].value, form["pHidden"].value,declarations.store_info['db_name'])
		
		if dbResult['status'] != 'success':
			ecommerce.alertsArea(form, "Could not connect to the database\n" + dbResult['message']);

		else:
			db = dbResult['result']

			sqlStatement = ecommerce.selectAllColumnsSqlStatement(table_data,'sales_tax_by_state',form["key_id"].value,'state_abbreviation')

			#print sqlStatement

			dbResult = ecommerce.executeSQL(db, sqlStatement)

			if dbResult['status'] != 'success':

				ecommerce.alertsArea(form, "Could not retrieve sales tax data to edit\n" + dbResult['message']);

			else:

				result = dbResult['result']

				table_data = ecommerce.dbToTableData(table_data, 'sales_tax_by_state', result[0])

				ecommerce.display_form(table_data, 'sales_tax_by_state', 1, 'useValues', 1, db)
				
				ecommerce.alertsArea(form, "Sales tax data retrieved successfully");

		ecommerce.editFunctionButtons(form["key_id"].value, '/' + declarations.store_info['db_name'] + '-cgi-bin/sales_tax_admin.pyc?username=' + form["uHidden"].value + '&password=' + form["pHidden"].value + '&performDbQuery=1', declarations.store_info['help_file'])

		ecommerce.editHiddenFields(form["uHidden"].value, form["pHidden"].value)
		
		print "</FORM>"

		ecommerce.trailer(table_data, db)
		db.close()
		
		print "</BODY>"
		print "</HTML>"
		
	elif form["action"].value == "query":

		query_sales_tax(1)

	elif form["action"].value == "delete":

		dbResult = ecommerce.connectDB(form["uHidden"].value, form["pHidden"].value,declarations.store_info['db_name'])
		
		if dbResult['status'] != 'success':
			onQueryLoad = 'displayWindow("Could not connect to the database")'

		else:
			db = dbResult['result']

			sqlStatement = "DELETE FROM sales_tax_by_state WHERE state_abbreviation = '" + form["key_id"].value + "'"

			dbResult = ecommerce.executeSQL(db, sqlStatement)

			if dbResult['status'] != 'success':

				onQueryLoad = "return displayWindow('Could not delete sales tax for state')"

			else:

				onQueryLoad = "return displayWindow('Sales tax for state successfully deleted')"

			db.close()

			query_sales_tax(1)

	elif form["action"].value == "save":

		table_data = declarations.define_tables()

		print "<HTML>"
		print "<HEAD>"

		ecommerce.generate_form_javascript(table_data,'sales_tax_by_state','sales_tax_admin',0,0)

		ecommerce.title("Sales Tax Administration")

		print "</HEAD>" 

		ecommerce.bodySetup()

		ecommerce.mainHeading('Sales Tax Administration')

		ecommerce.subHeading('Edit Sales Tax')

		ecommerce.formSetup("sales_tax_admin","sales_tax_admin","return submitForm(document.sales_tax_admin)",declarations.store_info['db_name'])

		dbResult = ecommerce.connectDB(form["uHidden"].value, form["pHidden"].value,declarations.store_info['db_name'])

		if dbResult['status'] != 'success':

			 ecommerce.alertsArea(form,"Sales tax data could not be saved, could not connect to db" + dbResult['message'])

		else:

			db = dbResult['result']

			if form["key_id"].value == 'create':

					form["key_id"].value = form['state_abbreviation'].value

			# save the Form
			dbResult = ecommerce.saveForm(table_data, db, None, "sales_tax_by_state", " WHERE state_name = '" + form["key_id"].value + "'", form)

			# if the form was not successfully saved
			if dbResult['status'] != 'success':
				ecommerce.alertsArea(form,"Sales tax data could not be saved due to an error during save,\n" + dbResult['message'] )

			# form was successfully saved
			else:

				table_data = declarations.define_tables()
				table_data = ecommerce.formToTableData(table_data,'sales_tax_by_state', form)

				ecommerce.display_form(table_data, 'sales_tax_by_state', 1, 'useValues', 1, db)
			
				ecommerce.alertsArea(form,"Sales tax data successfully saved")


		# generate function button row
		ecommerce.editFunctionButtons(form["key_id"].value, '/' + declarations.store_info['db_name'] + '-cgi-bin/sales_tax_admin.pyc?username=' + form["uHidden"].value + '&password=' + form["pHidden"].value + '&performDbQuery=1', declarations.store_info['help_file'])
			
		# generate hidden fields for form
		ecommerce.createHiddenFields(form["uHidden"].value, form["pHidden"].value)
			
		print "</FORM>"

		ecommerce.trailer(table_data, db)
		db.close()

		print "</BODY>"
		print "</HTML>"
			
	# create button was pressed on form
	elif form["action"].value == "create":

		print "<HTML>"
		print "<HEAD>"

		table_data = declarations.define_tables()

		ecommerce.generate_form_javascript(table_data,'sales_tax_by_state','sales_tax_admin',0,0)

		ecommerce.title("Create Sales Tax Data")

		print "</HEAD>" 

		ecommerce.bodySetup()

		ecommerce.mainHeading('Sales Tax Administration')

		ecommerce.subHeading('Create Sales Tax Data')

		ecommerce.formSetup("sales_tax_admin","sales_tax_admin","return submitForm(document.sales_tax_admin)",declarations.store_info['db_name'])

		# initialize form data values to zero or blank
		table_data = ecommerce.init_table_data(table_data,'sales_tax_by_state')

		# attempt to connect to db
		dbResult = ecommerce.connectDB(form["uHidden"].value,form["pHidden"].value,declarations.store_info['db_name'])
		
		# if db connection failed
		if dbResult['status'] != 'success':

			# generate appropriate message in alerts area
			 ecommerce.alertsArea(form,"Sales tax data could not be created, could not connect to db,\n" + dbResult['message'])			

		# else db connection succeeded
		else:

			# assign db connection variable
			db = dbResult['result']

			ecommerce.display_form(table_data, 'sales_tax_by_state', 1,'useValues',1,db)
				
		# display alerts area to create
		ecommerce.alertsArea(form,"Enter information on form and depress Create button")

		# create functions button row
		ecommerce.createFunctionButtons('create', '/' + declarations.store_info['db_name'] + '-cgi-bin/sales_tax_admin.pyc?username=' + form["uHidden"].value + '&password=' + form["pHidden"].value + '&performDbQuery=1', declarations.store_info['help_file'])

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

		ecommerce.generate_form_javascript(table_data,'sales_tax_by_state','sales_tax_admin',0,0)

		ecommerce.title("View Sales Tax for the State " + form['key_id'].value)

		print "</HEAD>" 

		ecommerce.bodySetup()

		ecommerce.mainHeading('Sales Tax Administration')
	
		ecommerce.subHeading('View Sales Tax')

		ecommerce.formSetup("sales_tax_admin","sales_tax_admin","return submitForm(document.sales_tax_admin)",declarations.store_info['db_name'])

		# attempt to connect to db
		dbResult = ecommerce.connectDB(form["uHidden"].value,form["pHidden"].value,declarations.store_info['db_name'])
		
		# if db connection failed
		if dbResult['status'] != 'success':

			# generate appropriate message in alerts area
			 ecommerce.alertsArea(form,"Sales tax data could not be viewed, could not connect to db,\n" + dbResult['message'])			

		# else db connection succeeded
		else:

			# assign db connection variable
			db = dbResult['result']

			sqlStatement = ecommerce.selectAllColumnsSqlStatement(table_data,'sales_tax_by_state',form["key_id"].value,'state_abbreviation')

			# execute select to retrieve customer ad data
			dbResult = ecommerce.executeSQL(db, sqlStatement)

			# if select failed
			if dbResult['status'] != 'success':
				
				# generate error in alerts area
				ecommerce.alertsArea(form,"Sales tax data could not be retrieved,\n" + dbResult['message'])

			# else select succeeded
			else:
				# assign result data
				result = dbResult['result']

				table_data = ecommerce.dbToTableData(table_data, 'sales_tax_by_state', result[0])

				ecommerce.display_form(table_data, 'sales_tax_by_state', 0)

		ecommerce.viewFunctionButtons('/' + declarations.store_info['db_name'] + '-cgi-bin/sales_tax_admin.pyc?username=' + form["uHidden"].value + '&password=' + form["pHidden"].value + '&performDbQuery=1', declarations.store_info['help_file'])

		print '</FORM>'
		
		ecommerce.trailer(table_data, db)
		db.close()
		print "</BODY>"
		print "</HTML>"

else:

	query_sales_tax(0)
