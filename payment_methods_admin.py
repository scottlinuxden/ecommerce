# $Id: payment_methods_admin.py,v 1.6 2000/04/06 00:38:25 davis Exp $
# Copyright (C) 1999 LinuXden, All Rights Reserved
# Copright Statement at http://www.linuxden.com/copyrighted_apps.html
# 
import os, string, sys
import cgi, glob
from pg import DB
import ecommerce
import declarations

ecommerce.htmlContentType()

def query_payment_methods(performDbQuery=0, onLoad=None, queryFields=None):

	table_data = declarations.define_tables()

	print "<HTML>"
	print "<HEAD>"

	ecommerce.javaScript("payment_methods_admin", 1)

	ecommerce.title("Payment Methods Administration")

	print "</HEAD>"

	ecommerce.bodySetup(onLoad)

	ecommerce.mainHeading('Payment Methods Administration')

	ecommerce.subHeading('Payment Methods')

	ecommerce.formSetup("payment_methods_admin","payment_methods_admin","return submitForm(document.payment_methods_admin)",declarations.store_info['db_name'])

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
			
			queryFields, whereFields = ecommerce.getQueryWhereFields(form, table_data, 'payment_methods')

			if queryFields == None or queryFields == []:
				queryFields = []
				whereFields = None
				queryFields.append('payment_type')

			dbResult, queryStatement = ecommerce.executeQuery(db, table_data, 'payment_methods', queryFields, whereFields, 'query', ecommerce.queryItemFunctionsHtmlNoEdit, 'ORDER by payment_type','payment_type')

			# if query was not successful
			if dbResult['status'] != 'success':
				ecommerce.alertsArea(form, "Could not retrieve credit card types data from database,\n" + dbResult['message']);
			# else payment methods retrieved ok
			else:
				ecommerce.alertsArea(form, "Last Query Statement: " + queryStatement + "\n" + `len(dbResult['result'])` + " payment methods retrieved from database");
				
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

		ecommerce.generate_form_javascript(table_data,'payment_methods','payment_methods_admin',0,0)

		ecommerce.title("Payment Method Administration")
		
		print "</HEAD>" 

		ecommerce.bodySetup()

		ecommerce.mainHeading('Payment Method Administration')
		
		ecommerce.subHeading('Edit Payment Methods')

		ecommerce.formSetup("payment_methods_admin","payment_methods_admin","return submitForm(document.payment_methods_admin)",declarations.store_info['db_name'])

		dbResult = ecommerce.connectDB(form["uHidden"].value, form["pHidden"].value,declarations.store_info['db_name'])
		
		if dbResult['status'] != 'success':
			ecommerce.alertsArea(form, "Could not connect to the database\n" + dbResult['message']);

		else:
			db = dbResult['result']

			sqlStatement = ecommerce.selectAllColumnsSqlStatement(table_data,'payment_methods',form["key_id"].value,'payment_type')

			#print sqlStatement

			dbResult = ecommerce.executeSQL(db, sqlStatement)

			if dbResult['status'] != 'success':

				ecommerce.alertsArea(form, "Could not retrieve Payment Methods to edit\n" + dbResult['message']);

			else:

				result = dbResult['result']

				table_data = ecommerce.dbToTableData(table_data, 'payment_methods', result[0])

				ecommerce.display_form(table_data, 'payment_methods', 1, 'useValues', 1, db)
				
				ecommerce.alertsArea(form, "Payment Methods retrieved successfully");


		ecommerce.editFunctionButtons(form["key_id"].value, '/' + declarations.store_info['db_name'] + '-cgi-bin/payment_methods_admin.pyc?username=' + form["uHidden"].value + '&password=' + form["pHidden"].value + '&performDbQuery=1', declarations.store_info['help_file'])

		ecommerce.editHiddenFields(form["uHidden"].value, form["pHidden"].value)
		
		print "</FORM>"

		ecommerce.trailer(table_data, db)

		# close db
		db.close()
		
		print "</BODY>"
		print "</HTML>"
		
	elif form["action"].value == "query":

		query_payment_methods(1)

	elif form["action"].value == "delete":

		dbResult = ecommerce.connectDB(form["uHidden"].value, form["pHidden"].value,declarations.store_info['db_name'])
		
		if dbResult['status'] != 'success':
			onQueryLoad = 'displayWindow("Could not connect to the database")'

		else:
			db = dbResult['result']

			sqlStatement = "DELETE FROM payment_methods WHERE payment_type = '" + form["key_id"].value + "'"

			dbResult = ecommerce.executeSQL(db, sqlStatement)

			if dbResult['status'] != 'success':

				onQueryLoad = "return displayWindow('Could not delete Payment Method')"

			else:

				onQueryLoad = "return displayWindow('Payment Method successfully deleted')"

			query_payment_methods(1)

	elif form["action"].value == "save":

		table_data = declarations.define_tables()

		print "<HTML>"
		print "<HEAD>"

		ecommerce.generate_form_javascript(table_data,'payment_methods','payment_methods_admin',0,0)

		ecommerce.title("Payment Method Administration")

		print "</HEAD>" 

		ecommerce.bodySetup()

		ecommerce.mainHeading('Payment Method Administration')

		ecommerce.subHeading('Edit Payment Method')

		ecommerce.formSetup("payment_methods_admin","payment_methods_admin","return submitForm(document.payment_methods_admin)",declarations.store_info['db_name'])

		dbResult = ecommerce.connectDB(form["uHidden"].value, form["pHidden"].value,declarations.store_info['db_name'])

		if dbResult['status'] != 'success':

			 ecommerce.alertsArea(form,"Payment Method could not be saved, could not connect to db" + dbResult['message'])

		else:

			db = dbResult['result']

			if form["key_id"].value == 'create':

					form["key_id"].value = form['payment_type'].value

			# save the Form
			dbResult = ecommerce.saveForm(table_data, db, None, "payment_methods", " WHERE payment_type = '" + form["key_id"].value + "'", form)

			# if the form was not successfully saved
			if dbResult['status'] != 'success':
				ecommerce.alertsArea(form,"Payment Method could not be saved due to an error during save,\n" + dbResult['message'] )

			# form was successfully saved
			else:

				table_data = declarations.define_tables()
				table_data = ecommerce.formToTableData(table_data,'payment_methods', form)

				ecommerce.display_form(table_data, 'payment_methods', 1, 'useValues', 1, db)
			
				ecommerce.alertsArea(form,"Payment Method successfully saved")

		# generate function button row
		ecommerce.editFunctionButtons(form["key_id"].value, '/' + declarations.store_info['db_name'] + '-cgi-bin/payment_methods_admin.pyc?username=' + form["uHidden"].value + '&password=' + form["pHidden"].value + '&performDbQuery=1', declarations.store_info['help_file'])
			
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

		ecommerce.generate_form_javascript(table_data,'payment_methods','payment_methods_admin',0,0)

		ecommerce.title("Create Payment Method")

		print "</HEAD>" 

		ecommerce.bodySetup()

		ecommerce.mainHeading('Payment Method Administration')

		ecommerce.subHeading('Create Payment Method')

		ecommerce.formSetup("payment_methods_admin","payment_methods_admin","return submitForm(document.payment_methods_admin)",declarations.store_info['db_name'])

		# initialize form data values to zero or blank
		table_data = ecommerce.init_table_data(table_data,'payment_methods')

		# attempt to connect to db
		dbResult = ecommerce.connectDB(form["uHidden"].value,form["pHidden"].value,declarations.store_info['db_name'])
		
		# if db connection failed
		if dbResult['status'] != 'success':

			# generate appropriate message in alerts area
			 ecommerce.alertsArea(form,"Payment Method could not be created, could not connect to db,\n" + dbResult['message'])			

		# else db connection succeeded
		else:

			# assign db connection variable
			db = dbResult['result']

			ecommerce.display_form(table_data, 'payment_methods', 1,'useValues',1,db)
				
		# display alerts area to create
		ecommerce.alertsArea(form,"Enter information on form and depress Create button")

		# create functions button row
		ecommerce.createFunctionButtons('create', '/' + declarations.store_info['db_name'] + '-cgi-bin/payment_methods_admin.pyc?username=' + form["uHidden"].value + '&password=' + form["pHidden"].value + '&performDbQuery=1', declarations.store_info['help_file'])

		# create hidden fields for form
		ecommerce.createHiddenFields(form["uHidden"].value, form["pHidden"].value)

		print "</FORM>"
		ecommerce.trailer(table_data, db)

		# close db
		db.close()

		print "</BODY>"
		print "</HTML>"

	# view button pressed
	elif form["action"].value == "view":

		table_data = declarations.define_tables()

		print "<HTML>"
		print "<HEAD>"

		ecommerce.generate_form_javascript(table_data,'payment_methods','payment_methods_admin',0,0)

		ecommerce.title("View Payment Method Data for " + form['key_id'].value)

		print "</HEAD>" 

		ecommerce.bodySetup()

		ecommerce.mainHeading('Payment Method Administration')
	
		ecommerce.subHeading('View Payment Method')

		ecommerce.formSetup("payment_methods_admin","payment_methods_admin","return submitForm(document.payment_methods_admin)",declarations.store_info['db_name'])

		# attempt to connect to db
		dbResult = ecommerce.connectDB(form["uHidden"].value,form["pHidden"].value,declarations.store_info['db_name'])
		
		# if db connection failed
		if dbResult['status'] != 'success':

			# generate appropriate message in alerts area
			 ecommerce.alertsArea(form,"Payment Method could not be viewed, could not connect to db,\n" + dbResult['message'])			

		# else db connection succeeded
		else:

			# assign db connection variable
			db = dbResult['result']

			sqlStatement = ecommerce.selectAllColumnsSqlStatement(table_data,'payment_methods',form["key_id"].value,'payment_type')

			# execute select to retrieve customer ad data
			dbResult = ecommerce.executeSQL(db, sqlStatement)

			# if select failed
			if dbResult['status'] != 'success':
				
				# generate error in alerts area
				ecommerce.alertsArea(form,"Payment Method data could not be retrieved,\n" + dbResult['message'])

			# else select succeeded
			else:
				# assign result data
				result = dbResult['result']

				table_data = ecommerce.dbToTableData(table_data, 'payment_methods', result[0])

				ecommerce.display_form(table_data, 'payment_methods', 0)

		ecommerce.viewFunctionButtons('/' + declarations.store_info['db_name'] + '-cgi-bin/payment_methods_admin.pyc?username=' + form["uHidden"].value + '&password=' + form["pHidden"].value + '&performDbQuery=1', declarations.store_info['help_file'])

		print '</FORM>'

		ecommerce.trailer(table_data, db)

		# close db
		db.close()

		print "</BODY>"
		print "</HTML>"

else:

	query_payment_methods(0)




