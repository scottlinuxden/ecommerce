# $Id: customer_property_admin.py,v 1.6 2000/04/06 00:31:13 davis Exp davis $
# Copyright (C) 1999 LinuXden, All Rights Reserved
# Copright Statement at http://www.linuxden.com/copyrighted_apps.html
# 
import os, string, sys
import cgi, glob
from pg import DB
import declarations
import ecommerce

ecommerce.htmlContentType()

help_pdf = declarations.store_info['help_file']

def queryCustomerItemHtml(db_key):
	return '<TD ALIGN=CENTER NOWRAP><INPUT NAME="edit" type="button" value=" Edit " onClick="return execute(' + "'edit'" + ", '" + db_key + "'" + ')"><INPUT NAME="view" type="button" value=" View " onClick="return execute(' + "'view'" + ", '" + db_key + "'" + ')">'

def query_properties(performDbQuery=0, onLoad=None, queryFields=None):

	table_data = declarations.define_tables()

	print "<HTML>"
	print "<HEAD>"

	ecommerce.javaScript("customer_property_admin", 1)

	ecommerce.title("Customer Property Administration")

	print "</HEAD>"

	ecommerce.bodySetup(onLoad)

	print '<CENTER>'
	print '<TABLE COLS=1 WIDTH=585>'
	print '<TR><TD>'

	ecommerce.mainHeading('Customer Property Administration')

	ecommerce.subHeading('Property Listing')

	ecommerce.formSetup("customer_property_admin","customer_property_admin","return submitForm(document.customer_property_admin)",declarations.store_info['db_name'])

	if form.has_key("customer_id"):
		customer_id = form["customer_id"].value
	else:
		if form.has_key("cHidden"):
			customer_id = form["cHidden"].value
		else:
			customer_id = ''

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

	print '<TABLE><BORDER=0>'
	print '<TR>'

	ecommerce.tableColumn('<B>Customer ID:</B>')
	print '<TD ALIGN=CENTER NOWRAP>'

	ecommerce.textbox(None,'customer_id',customer_id,'10','10',"checkBlankField(this, 'Customer ID')","displayHint('Enter your customer id')")
	print '</TD>'

	ecommerce.tableColumn('<B>Username:</B>')
	print '<TD ALIGN=CENTER NOWRAP>'

	ecommerce.textbox(None,'username',username,'9','9',"checkBlankField(this, 'Username')","displayHint('Enter your username')")
	print '</TD>'

	ecommerce.tableColumn('<B>Password:</B>')

	print '<TD ALIGN=CENTER NOWRAP>'

	ecommerce.textbox(None,'password',password,'8','8',"checkBlankField(this, 'Password')","displayHint('Enter your password')",'password')

	print '</TD>'
	print '</TR>'
	print '</TABLE>'

	if form.has_key("performDbQuery") or performDbQuery == 1:

		dbResult = ecommerce.connectDB(
			declarations.store_info['browser_username'], 
			declarations.store_info['browser_password'], 
			declarations.store_info['db_name'])
		
		# could not connect to db
		if dbResult['status'] != 'success':
			
			ecommerce.alertsArea(form, "Can not connect to database,\n" + dbResult['message'])
			
			print '<HR>'
			print '<TABLE>'
			print '<TR>'
			ecommerce.tableColumn('<INPUT NAME="query" type="button" value=" Query " onClick="return execute(' + "'query'" + ')">')
			ecommerce.tableColumn('<INPUT TYPE="button" NAME="help" VALUE=" Help " onClick="return goto_url (' + "'" + help_pdf + "'" + ')">')
			print '</TR>'
			print '</TABLE>'

		else:

			db = dbResult['result']

			# validate username password and customer id
			dbResult = ecommerce.executeSQL(db, "SELECT count(*) FROM customers WHERE id = '" + string.strip(customer_id) + "' AND account_username = '" + username + "' AND account_password = '" + password + "'")

			if dbResult['status'] != 'success':

				ecommerce.alertsArea(form, "Could not validate customer information provided\n" + dbResult['message']);

				ecommerce.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
				ecommerce.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
				ecommerce.textbox(None, 'cHidden', customer_id, '10', '10', None, None, 'hidden')
				ecommerce.textbox(None, 'uHidden', username, '9', '9', None, None, 'hidden')
				ecommerce.textbox(None, 'pHidden', password, '8', '8', None, None, 'hidden')
				
				print "</FORM>"
				
				ecommerce.trailer(table_data, db)

				print '</TD>'
				print '</TR>'
				print '</TABLE>'
				print '</CENTER>'

				print "</BODY>"
				print "</HTML>"

			else:

				result = dbResult['result']

				if result[0]['count'] != 1:
					ecommerce.alertsArea(form, "Could not validate customer information provided\n" + dbResult['message']);
					print '<HR>'
					print '<TABLE>'
					print '<TR>'
					ecommerce.tableColumn('<INPUT NAME="query" type="button" value=" Query " onClick="return execute(' + "'query'" + ')">')
					ecommerce.tableColumn('<INPUT TYPE="button" NAME="help" VALUE=" Help " onClick="return goto_url (' + "'" + help_pdf + "'" + ')">')
					print '</TR>'
					print '</TABLE>'

					ecommerce.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
					ecommerce.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
					ecommerce.textbox(None, 'cHidden', customer_id, '10', '10', None, None, 'hidden')
					ecommerce.textbox(None, 'uHidden', username, '9', '9', None, None, 'hidden')
					ecommerce.textbox(None, 'pHidden', password, '8', '8', None, None, 'hidden')
					
					print "</FORM>"
					
					ecommerce.trailer(table_data, db)

					print '</TD>'
					print '</TR>'
					print '</TABLE>'
					print '</CENTER>'

					print "</BODY>"
					print "</HTML>"
					
					sys.exit(1)

			queryFields, whereFields = ecommerce.getQueryWhereFields(form, table_data, 'properties')

			if queryFields == None or queryFields == []:
				queryFields = []
				whereFields = None
				queryFields.append('id')
				queryFields.append('town')
				queryFields.append('style')
				queryFields.append('bedrooms')
				queryFields.append('price')

			dbResult, queryStatement = ecommerce.executeQuery(db, 
													table_data, 
													'properties', 
													queryFields, 
													whereFields, 
													'query',
													queryCustomerItemHtml,
													'ORDER BY id',
													'id',
													"customer_id='" + customer_id + "' and display_property = 't'")

			# if query was not successful
			if dbResult['status'] != 'success':
				ecommerce.alertsArea(form, "Could not retrieve properties from database,\n" + dbResult['message']);
			# else properties were retrieved ok
			else:
				ecommerce.alertsArea(form, "Last Query Statement: " + queryStatement + "\n" + `len(dbResult['result'])` + " properties retrieved from database");
				
			print '<HR>'
			print '<TABLE>'
			print '<TR>'
			ecommerce.tableColumn('<INPUT NAME="query" type="button" value=" Query " onClick="return execute(' + "'query'" + ')">')
			ecommerce.tableColumn('<INPUT TYPE="button" NAME="help" VALUE=" Help " onClick="return goto_url (' + "'" + help_pdf + "'" + ')">')
			print '</TR>'
			print '</TABLE>'

	else:
		print '<HR>'
		print '<TABLE>'
		print '<TR>'
		ecommerce.tableColumn('<INPUT NAME="query" type="button" value=" Query " onClick="return execute(' + "'query'" + ')">')
		ecommerce.tableColumn('<INPUT TYPE="button" NAME="help" VALUE=" Help " onClick="return goto_url (' + "'" + help_pdf + "'" + ')">')
		print '</TR>'
		print '</TABLE>'

	ecommerce.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
	ecommerce.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
	ecommerce.textbox(None, 'cHidden', customer_id, '10', '10', None, None, 'hidden')
	ecommerce.textbox(None, 'uHidden', username, '9', '9', None, None, 'hidden')
	ecommerce.textbox(None, 'pHidden', password, '8', '8', None, None, 'hidden')

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
		
		table_data['properties']['customer_id']['display'] = 'read-only'
		table_data['properties']['order_id']['display'] = 'read-only'
		table_data['properties']['display_property']['display'] = 'Hidden'

		ecommerce.generate_form_javascript(table_data,'properties','customer_property_admin',0,0)

		ecommerce.title("Customer Property Administration")
		
		print "</HEAD>" 

		ecommerce.bodySetup()

		ecommerce.mainHeading('Customer Property Administration')
		
		ecommerce.subHeading('Edit Property')

		ecommerce.formSetup("customer_property_admin","customer_property_admin","return submitForm(document.customer_property_admin)",declarations.store_info['db_name'])

		dbResult = ecommerce.connectDB(
			declarations.store_info['browser_username'],
			declarations.store_info['browser_password'],
			declarations.store_info['db_name'])
		
		if dbResult['status'] != 'success':
			ecommerce.alertsArea(form, "Could not connect to the database\n" + dbResult['message']);

		else:
			db = dbResult['result']

			# validate username password and customer id
			dbResult = ecommerce.executeSQL(db, "SELECT count(*) FROM customers WHERE id = '" + string.strip(form['cHidden'].value) + "' AND account_username = '" + form['uHidden'].value + "' AND account_password = '" + form['pHidden'].value + "'")

			if dbResult['status'] != 'success':

				ecommerce.alertsArea(form, "Could not validate customer information provided\n" + dbResult['message']);

			else:

				result = dbResult['result']

				if result[0]['count'] != 1:
					ecommerce.alertsArea(form, "Could not validate customer information provided\n" + dbResult['message']);
					print '<HR>'
					print '<TABLE>'
					print '<TR>'
					ecommerce.tableColumn('<INPUT NAME="query" type="button" value=" Query " onClick="return execute(' + "'query'" + ')">')
					ecommerce.tableColumn('<INPUT TYPE="button" NAME="help" VALUE=" Help " onClick="return goto_url (' + "'" + help_pdf + "'" + ')">')
					print '</TR>'
					print '</TABLE>'
					sys.exit(1)


			sqlStatement = ecommerce.selectAllColumnsSqlStatement(table_data,'properties',form["key_id"].value)

			dbResult = ecommerce.executeSQL(db, sqlStatement)

			if dbResult['status'] != 'success':

				ecommerce.alertsArea(form, "Could not retrieve property data to edit\n" + dbResult['message']);

			else:

				result = dbResult['result']

				table_data = ecommerce.dbToTableData(table_data, 'properties', result[0])

				ecommerce.display_form(table_data, 'properties', 1, 'useValues', 1, db)
				
				ecommerce.alertsArea(form, "Property data retrieved successfully");

		db_key = form['key_id'].value
		menu_name =  '/'  + declarations.store_info['db_name'] + '-cgi-bin/customer_property_admin.pyc?customer_id=' + form['cHidden'].value + '&username=' + form["uHidden"].value + '&password=' + form["pHidden"].value + '&performDbQuery=1'
		help_pdf = declarations.store_info['help_file']

		print '<HR>'
		print '<TABLE>'
		print '<TR>'
		ecommerce.tableColumn('<INPUT NAME="save" type="button" value=" Save " onClick="return execute(' + "'save'" + ",'" + db_key + "'" + ')">')
		ecommerce.tableColumn('<INPUT NAME="view" type="button" value=" View " onClick="return execute(' + "'view'" + ", '" + db_key + "'" + ')">')
		ecommerce.tableColumn('<INPUT TYPE="button" NAME="return_to_menu" VALUE=" Listing " onClick="return goto_url (' + "'" + menu_name + "'" + ')">')
		ecommerce.tableColumn('<INPUT TYPE="button" NAME="help" VALUE=" Help " onClick="return goto_url (' + "'" + help_pdf + "'" + ')">')
		print '</TR>'
		print '</TABLE>'

		ecommerce.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
		ecommerce.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
		ecommerce.textbox(None, 'cHidden', form['cHidden'].value, '10', '10', None, None, 'hidden')
		ecommerce.textbox(None, 'uHidden', form['uHidden'].value, '9', '9', None, None, 'hidden')
		ecommerce.textbox(None, 'pHidden', form['pHidden'].value, '8', '8', None, None, 'hidden')
		ecommerce.textbox(None, 'oHidden', table_data['properties']['order_id']['value'], '10', '10', None, None, 'hidden')
		
		print "</FORM>"

		ecommerce.trailer(table_data, db)

		# close db
		db.close()
		
		print "</BODY>"
		print "</HTML>"
		
	elif form["action"].value == "query":

		query_properties(1)

	elif form["action"].value == "save":

		table_data = declarations.define_tables()

		print "<HTML>"
		print "<HEAD>"

		table_data['properties']['customer_id']['display'] = 'read-only'
		table_data['properties']['customer_id']['value'] = form['cHidden'].value
		table_data['properties']['order_id']['display'] = 'read-only'
		table_data['properties']['order_id']['value'] = form['oHidden'].value
		table_data['properties']['display_property']['display'] = 'Hidden'

		ecommerce.generate_form_javascript(table_data,'properties','customer_property_admin',0,0)
		
		ecommerce.title("Customer Property Administration")

		print "</HEAD>" 

		ecommerce.bodySetup()

		ecommerce.mainHeading('Customer Property Administration')

		ecommerce.subHeading('Edit Property')

		ecommerce.formSetup("customer_property_admin","customer_property_admin","return submitForm(document.customer_property_admin)",declarations.store_info['db_name'])

		dbResult = ecommerce.connectDB(
			declarations.store_info['browser_username'],
			declarations.store_info['browser_password'],
			declarations.store_info['db_name'])

		if dbResult['status'] != 'success':

			 ecommerce.alertsArea(form,"Property data could not be saved, could not connect to db" + dbResult['message'])

		else:

			db = dbResult['result']

			# validate username password and customer id
			dbResult = ecommerce.executeSQL(db, "SELECT count(*) FROM customers WHERE id = '" + string.strip(form['cHidden'].value) + "' AND account_username = '" + form['uHidden'].value + "' AND account_password = '" + form['pHidden'].value + "'")

			if dbResult['status'] != 'success':

				ecommerce.alertsArea(form, "Could not validate customer information provided\n" + dbResult['message']);

			else:

				result = dbResult['result']

				if result[0]['count'] != 1:
					ecommerce.alertsArea(form, "Could not validate customer information provided\n" + dbResult['message']);
					print '<HR>'
					print '<TABLE>'
					print '<TR>'
					ecommerce.tableColumn('<INPUT NAME="query" type="button" value=" Query " onClick="return execute(' + "'query'" + ')">')
					ecommerce.tableColumn('<INPUT TYPE="button" NAME="help" VALUE=" Help " onClick="return goto_url (' + "'" + help_pdf + "'" + ')">')
					print '</TR>'
					print '</TABLE>'
					sys.exit(1)

			# save the Form
			dbResult = ecommerce.saveForm(table_data, db, form["key_id"].value, "properties", " WHERE id = '" + form["key_id"].value + "'", form)

			# if the form was not successfully saved
			if dbResult['status'] != 'success':
				ecommerce.alertsArea(form,"Property data could not be saved due to an error during save,\n" + dbResult['message'] )

			# form was successfully saved
			else:

				table_data = ecommerce.formToTableData(table_data,'properties', form, form["key_id"].value)

				ecommerce.display_form(table_data, 'properties', 1, 'useValues', 1, db)
			
				ecommerce.alertsArea(form,"Property data successfully saved")

		# generate function button row
		db_key = form['key_id'].value
		menu_name =  '/' + declarations.store_info['db_name'] + '-cgi-bin/customer_property_admin.pyc?customer_id=' + form['cHidden'].value + '&username=' + form["uHidden"].value + '&password=' + form["pHidden"].value + '&performDbQuery=1'
		help_pdf = declarations.store_info['help_file']

		print '<HR>'
		print '<TABLE>'
		print '<TR>'
		ecommerce.tableColumn('<INPUT NAME="save" type="button" value=" Save " onClick="return execute(' + "'save'" + ",'" + db_key + "'" + ')">')
		ecommerce.tableColumn('<INPUT NAME="view" type="button" value=" View " onClick="return execute(' + "'view'" + ", '" + db_key + "'" + ')">')
		ecommerce.tableColumn('<INPUT TYPE="button" NAME="return_to_menu" VALUE=" Listing " onClick="return goto_url (' + "'" + menu_name + "'" + ')">')
		ecommerce.tableColumn('<INPUT TYPE="button" NAME="help" VALUE=" Help " onClick="return goto_url (' + "'" + help_pdf + "'" + ')">')
		print '</TR>'
		print '</TABLE>'
			
		ecommerce.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
		ecommerce.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
		ecommerce.textbox(None, 'cHidden', form['cHidden'].value, '10', '10', None, None, 'hidden')
		ecommerce.textbox(None, 'uHidden', form['uHidden'].value, '9', '9', None, None, 'hidden')
		ecommerce.textbox(None, 'pHidden', form['pHidden'].value, '8', '8', None, None, 'hidden')
		ecommerce.textbox(None, 'oHidden', form['oHidden'].value, '10', '10', None, None, 'hidden')
			
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
		
		table_data['properties']['customer_id']['display'] = 'read-only'
		table_data['properties']['customer_id']['value'] = form['cHidden'].value
		table_data['properties']['order_id']['display'] = 'read-only'
			
		table_data['properties']['display_property']['display'] = 'Hidden'

		ecommerce.generate_form_javascript(table_data,'properties','customer_property_admin',0,0)

		ecommerce.title("View Property Listing Id " + form['key_id'].value)

		print "</HEAD>" 

		ecommerce.bodySetup()

		ecommerce.mainHeading('Customer Property Administration')
	
		ecommerce.subHeading('View Property')

		ecommerce.formSetup("customer_property_admin","customer_property_admin","return submitForm(document.customer_property_admin)",declarations.store_info['db_name'])

		# attempt to connect to db
		dbResult = ecommerce.connectDB(
			declarations.store_info['browser_username'],
			declarations.store_info['browser_password'],
			declarations.store_info['db_name'])
		
		# if db connection failed
		if dbResult['status'] != 'success':

			# generate appropriate message in alerts area
			 ecommerce.alertsArea(form,"Property data could not be viewed, could not connect to db,\n" + dbResult['message'])			

		# else db connection succeeded
		else:

			# assign db connection variable
			db = dbResult['result']

			# validate username password and customer id
			dbResult = ecommerce.executeSQL(db, "SELECT count(*) FROM customers WHERE id = '" + string.strip(form['cHidden'].value) + "' AND account_username = '" + form['uHidden'].value + "' AND account_password = '" + form['pHidden'].value + "'")

			if dbResult['status'] != 'success':

				ecommerce.alertsArea(form, "Could not validate customer information provided\n" + dbResult['message']);

			else:

				result = dbResult['result']

				if result[0]['count'] != 1:
					ecommerce.alertsArea(form, "Could not validate customer information provided\n" + dbResult['message']);
					print '<HR>'
					print '<TABLE>'
					print '<TR>'
					ecommerce.tableColumn('<INPUT NAME="query" type="button" value=" Query " onClick="return execute(' + "'query'" + ')">')
					ecommerce.tableColumn('<INPUT TYPE="button" NAME="help" VALUE=" Help " onClick="return goto_url (' + "'" + help_pdf + "'" + ')">')
					print '</TR>'
					print '</TABLE>'
					sys.exit(1)

			sqlStatement = ecommerce.selectAllColumnsSqlStatement(table_data,'properties',form["key_id"].value)

			# execute select to retrieve property ad data
			dbResult = ecommerce.executeSQL(db, sqlStatement)

			# if select failed
			if dbResult['status'] != 'success':
				
				# generate error in alerts area
				ecommerce.alertsArea(form,"Property data could not be retrieved,\n" + dbResult['message'])

			# else select succeeded
			else:
				# assign result data
				result = dbResult['result']

				table_data = ecommerce.dbToTableData(table_data, 'properties', result[0])

				ecommerce.display_form(table_data, 'properties', 0)

		menu_name = '/' + declarations.store_info['db_name'] + '-cgi-bin/customer_property_admin.pyc?customer_id=' + form['cHidden'].value + '&username=' + form["uHidden"].value + '&password=' + form["pHidden"].value + '&performDbQuery=1'
		help_pdf =  declarations.store_info['help_file']

		print '<HR>'
		print '<TABLE>'
		print '<TR>'
		ecommerce.tableColumn('<INPUT TYPE="button" NAME="return_to_menu" VALUE=" Listing " onClick="return goto_url (' + "'" + menu_name + "'" + ')">')
		ecommerce.tableColumn('<INPUT TYPE="button" NAME="help" VALUE=" Help " onClick="return goto_url (' + "'" + help_pdf + "'" + ')">')
		print '</TR>'
		print '</TABLE>'

		print '</FORM>'

		ecommerce.trailer(table_data, db)
		db.close()

		print "</BODY>"
		print "</HTML>"

else:

	query_properties(0)
