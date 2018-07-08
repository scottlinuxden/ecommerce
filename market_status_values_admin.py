# $Id: market_status_values_admin.py,v 1.7 2000/04/06 00:38:25 davis Exp $
# Copyright (C) 1999 LinuXden, All Rights Reserved
# Copright Statement at http://www.linuxden.com/copyrighted_apps.html
# 
import os, string, sys
import cgi, glob
from pg import DB
import ecommerce
import declarations

ecommerce.htmlContentType()

def query_market_status_values(performDbQuery=0, onLoad=None, queryFields=None):

	table_data = declarations.define_tables()

	print "<HTML>"
	print "<HEAD>"

	ecommerce.javaScript("market_status_values_admin", 1)

	ecommerce.title("Market Status Administration")

	print "</HEAD>"

	ecommerce.bodySetup(onLoad)

	ecommerce.mainHeading('Market Status Administration')

	ecommerce.subHeading('Market Status Values')

	ecommerce.formSetup("market_status_values_admin","market_status_values_admin","return submitForm(document.market_status_values_admin)",declarations.store_info['db_name'])

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
			
			queryFields, whereFields = ecommerce.getQueryWhereFields(form, table_data, 'market_status_values')

			if queryFields == None or queryFields == []:
				queryFields = []
				whereFields = None
				queryFields.append('status_of_market')

			dbResult, queryStatement = ecommerce.executeQuery(db, table_data, 'market_status_values', queryFields, whereFields, 'query', ecommerce.queryItemFunctionsHtmlNoEdit, 'ORDER by status_of_market','status_of_market')

			# if query was not successful
			if dbResult['status'] != 'success':
				ecommerce.alertsArea(form, "Could not retrieve market status values data from database,\n" + dbResult['message']);
			# else market status values data was retrieved ok
			else:
				ecommerce.alertsArea(form, "Last Query Statement: " + queryStatement + "\n" + `len(dbResult['result'])` + " market status value items retrieved from database");
				
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

		ecommerce.generate_form_javascript(table_data,'market_status_values','market_status_values_admin',0,0)

		ecommerce.title("Market Status Administration")
		
		print "</HEAD>" 

		ecommerce.bodySetup()

		ecommerce.mainHeading('Market Status Administration')
		
		ecommerce.subHeading('Edit Market Status Values')

		ecommerce.formSetup("market_status_values_admin","market_status_values_admin","return submitForm(document.market_status_values_admin)",declarations.store_info['db_name'])

		dbResult = ecommerce.connectDB(form["uHidden"].value, form["pHidden"].value,declarations.store_info['db_name'])
		
		if dbResult['status'] != 'success':
			ecommerce.alertsArea(form, "Could not connect to the database\n" + dbResult['message']);

		else:
			db = dbResult['result']

			sqlStatement = ecommerce.selectAllColumnsSqlStatement(table_data,'market_status_values',form["key_id"].value,'status_of_market')

			dbResult = ecommerce.executeSQL(db, sqlStatement)

			if dbResult['status'] != 'success':

				ecommerce.alertsArea(form, "Could not retrieve market status values to edit\n" + dbResult['message']);

			else:

				result = dbResult['result']

				table_data = ecommerce.dbToTableData(table_data, 'market_status_values', result[0])

				ecommerce.display_form(table_data, 'market_status_values', 1, 'useValues', 1, db)
				
				ecommerce.alertsArea(form, "Market Statuses retrieved successfully");

		ecommerce.editFunctionButtons(form["key_id"].value, '/' + declarations.store_info['db_name'] + '-cgi-bin/market_status_values_admin.pyc?username=' + form["uHidden"].value + '&password=' + form["pHidden"].value + '&performDbQuery=1', declarations.store_info['help_file'])

		ecommerce.editHiddenFields(form["uHidden"].value, form["pHidden"].value)
		
		print "</FORM>"

		ecommerce.trailer(table_data, db)

		# close db
		db.close()
		
		print "</BODY>"
		print "</HTML>"
		
	elif form["action"].value == "query":

		query_market_status_values(1)

	elif form["action"].value == "delete":

		dbResult = ecommerce.connectDB(form["uHidden"].value, form["pHidden"].value,declarations.store_info['db_name'])
		
		if dbResult['status'] != 'success':
			onQueryLoad = 'displayWindow("Could not connect to the database")'

		else:
			db = dbResult['result']

			sqlStatement = "DELETE FROM market_status_values WHERE status_of_market = '" + form["key_id"].value + "'"

			dbResult = ecommerce.executeSQL(db, sqlStatement)

			if dbResult['status'] != 'success':

				onQueryLoad = "return displayWindow('Could not delete market status value')"

			else:

				onQueryLoad = "return displayWindow('market status value successfully deleted')"

			query_market_status_values(1)

	elif form["action"].value == "save":

		table_data = declarations.define_tables()

		print "<HTML>"
		print "<HEAD>"

		ecommerce.generate_form_javascript(table_data,'market_status_values','market_status_values_admin',0,0)

		ecommerce.title("Market Status Administration")

		print "</HEAD>" 

		ecommerce.bodySetup()

		ecommerce.mainHeading('Market Status Administration')

		ecommerce.subHeading('Edit Market Status Values')

		ecommerce.formSetup("market_status_values_admin","market_status_values_admin","return submitForm(document.market_status_values_admin)",declarations.store_info['db_name'])

		dbResult = ecommerce.connectDB(form["uHidden"].value, form["pHidden"].value,declarations.store_info['db_name'])

		if dbResult['status'] != 'success':

			 ecommerce.alertsArea(form,"Market Status could not be saved, could not connect to db" + dbResult['message'])

		else:

			db = dbResult['result']

			if form["key_id"].value == 'create':

					form["key_id"].value = form['status_of_market'].value

			# save the Form
			dbResult = ecommerce.saveForm(table_data, db, None, "market_status_values", " WHERE status_of_market = '" + form["key_id"].value + "'", form)

			# if the form was not successfully saved
			if dbResult['status'] != 'success':
				ecommerce.alertsArea(form,"Market Status could not be saved due to an error during save,\n" + dbResult['message'] )

			# form was successfully saved
			else:

				table_data = declarations.define_tables()

				table_data = ecommerce.formToTableData(table_data,'market_status_values', form)

				ecommerce.display_form(table_data, 'market_status_values', 1, 'useValues', 1, db)
			
				ecommerce.alertsArea(form,"Market Status successfully saved")

		# generate function button row
		ecommerce.editFunctionButtons(form["key_id"].value, '/' + declarations.store_info['db_name'] + '-cgi-bin/market_status_values_admin.pyc?username=' + form["uHidden"].value + '&password=' + form["pHidden"].value + '&performDbQuery=1', declarations.store_info['help_file'])
			
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

		ecommerce.generate_form_javascript(table_data,'market_status_values','market_status_values_admin',0,0)

		ecommerce.title("Create Market Status")

		print "</HEAD>" 

		ecommerce.bodySetup()

		ecommerce.mainHeading('Market Status Administration')

		ecommerce.subHeading('Create Market Status')

		ecommerce.formSetup("market_status_values_admin","market_status_values_admin","return submitForm(document.market_status_values_admin)",declarations.store_info['db_name'])

		# initialize form data values to zero or blank
		table_data = ecommerce.init_table_data(table_data, 'market_status_values')

		# attempt to connect to db
		dbResult = ecommerce.connectDB(form["uHidden"].value,form["pHidden"].value,declarations.store_info['db_name'])
		
		# if db connection failed
		if dbResult['status'] != 'success':

			# generate appropriate message in alerts area
			 ecommerce.alertsArea(form,"Market Status could not be created, could not connect to db,\n" + dbResult['message'])			

		# else db connection succeeded
		else:

			# assign db connection variable
			db = dbResult['result']

			ecommerce.display_form(table_data, 'market_status_values', 1,'useValues',1,db)
				
		# display alerts area to create
		ecommerce.alertsArea(form,"Enter information on form and depress Create button")

		# create functions button row
		ecommerce.createFunctionButtons('create', '/' + declarations.store_info['db_name'] + '-cgi-bin/market_status_values_admin.pyc?username=' + form["uHidden"].value + '&password=' + form["pHidden"].value + '&performDbQuery=1', declarations.store_info['help_file'])

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

		ecommerce.generate_form_javascript(table_data,'market_status_values','market_status_values_admin',0,0)

		ecommerce.title("View Market Status Data for " + form['key_id'].value)

		print "</HEAD>" 

		ecommerce.bodySetup()

		ecommerce.mainHeading('Market Status Administration')
	
		ecommerce.subHeading('View Market Status')

		ecommerce.formSetup("market_status_values_admin","market_status_values_admin","return submitForm(document.market_status_values_admin)",declarations.store_info['db_name'])

		# attempt to connect to db
		dbResult = ecommerce.connectDB(form["uHidden"].value,form["pHidden"].value,declarations.store_info['db_name'])
		
		# if db connection failed
		if dbResult['status'] != 'success':

			# generate appropriate message in alerts area
			 ecommerce.alertsArea(form,"Market Status could not be viewed, could not connect to db,\n" + dbResult['message'])			

		# else db connection succeeded
		else:

			# assign db connection variable
			db = dbResult['result']

			sqlStatement = ecommerce.selectAllColumnsSqlStatement(table_data,'market_status_values',form["key_id"].value,'status_of_market')

			# execute select to retrieve customer ad data
			dbResult = ecommerce.executeSQL(db, sqlStatement)

			# if select failed
			if dbResult['status'] != 'success':
				
				# generate error in alerts area
				ecommerce.alertsArea(form,"Market Status data could not be retrieved,\n" + dbResult['message'])

			# else select succeeded
			else:
				# assign result data
				result = dbResult['result']

				table_data = ecommerce.dbToTableData(table_data, 'market_status_values', result[0])

				ecommerce.display_form(table_data, 'market_status_values', 0)

		ecommerce.viewFunctionButtons('/' + declarations.store_info['db_name'] + '-cgi-bin/market_status_values_admin.pyc?username=' + form["uHidden"].value + '&password=' + form["pHidden"].value + '&performDbQuery=1', declarations.store_info['help_file'])

		print '</FORM>'

		ecommerce.trailer(table_data, db)

		db.close()

		print "</BODY>"
		print "</HTML>"

else:

	query_market_status_values(0)
