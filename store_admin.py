# $Id: store_admin.py,v 1.6 2000/04/06 00:38:25 davis Exp $
# Copyright (C) 1999 LinuXden, All Rights Reserved
# Copright Statement at http://www.linuxden.com/copyrighted_apps.html
# 
import os, string, sys
import cgi, glob
from pg import DB
import ecommerce
import declarations

ecommerce.htmlContentType()

def storeButtons(button_name):
	print '<HR>'
	print '<TABLE>'
	print '<TR>'
	if button_name == 'edit':
		ecommerce.tableColumn('<INPUT NAME="edit" type="button" value=" Edit " onClick="return execute(' + "'edit'" + ",'1'" + ')">')
	elif button_name == 'save':
		ecommerce.tableColumn('<INPUT NAME="save" type="button" value=" Save " onClick="return execute(' + "'save'" + ",'1'" + ')">')
	ecommerce.tableColumn('<INPUT TYPE="button" NAME="help" VALUE=" Help " onClick="return goto_url (' + "'" + declarations.store_info['help_file'] + "'" + ')">')
	print '</TR>'
	print '</TABLE>'

def edit_store_info(performDbQuery=0, onLoad=None, queryFields=None):

	table_data = declarations.define_tables()

	print "<HTML>"
	print "<HEAD>"

	ecommerce.javaScript("store_admin", 1)

	ecommerce.title("Store Administration")

	print "</HEAD>"

	ecommerce.bodySetup(onLoad)

	ecommerce.mainHeading('Store Administration')

	ecommerce.subHeading('Store Info')

	ecommerce.formSetup("store_admin","store_admin","return submitForm(document.store_admin)",declarations.store_info['db_name'])

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

			storeButtons()

		else:
			db = dbResult['result']
			

			sqlStatement = ecommerce.selectAllColumnsSqlStatement(table_data,'store_info',form["key_id"].value)

			dbResult = ecommerce.executeSQL(db, sqlStatement)


			if dbResult['status'] != 'success':

				ecommerce.alertsArea(form, "Could not retrieve store information\n" + dbResult['message']);

			else:

				result = dbResult['result']

				table_data = ecommerce.dbToTableData(table_data, 'store_info', result[0])

				ecommerce.table_data['store_info']['id']['value'] = '1'

				ecommerce.display_form(table_data, 'store_info', 1, 'useValues', 1, db)
				
				ecommerce.alertsArea(form, "Store Information retrieved successfully");

		storeButtons(button_name='save')

		ecommerce.editHiddenFields(form["uHidden"].value, form["pHidden"].value)

	else:

		storeButtons(button_name='edit')

		ecommerce.editHiddenFields(username, password, '1')

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

		ecommerce.generate_form_javascript(table_data,'store_info','store_admin',0,0)

		ecommerce.title("Store Info Administration")
		
		print "</HEAD>" 

		ecommerce.bodySetup()

		ecommerce.mainHeading('Store Info Administration')
		
		ecommerce.subHeading('Edit Store Infos')

		ecommerce.formSetup("store_admin","store_admin","return submitForm(document.store_admin)",declarations.store_info['db_name'])

		dbResult = ecommerce.connectDB(form["uHidden"].value, form["pHidden"].value,declarations.store_info['db_name'])
		
		if dbResult['status'] != 'success':
			ecommerce.alertsArea(form, "Could not connect to the database\n" + dbResult['message']);

		else:
			db = dbResult['result']

			sqlStatement = ecommerce.selectAllColumnsSqlStatement(table_data,'store_info','1')

			#print sqlStatement

			dbResult = ecommerce.executeSQL(db, sqlStatement)

			if dbResult['status'] != 'success':

				ecommerce.alertsArea(form, "Could not retrieve store info to edit\n" + dbResult['message']);

			else:

				result = dbResult['result']

				table_data = ecommerce.dbToTableData(table_data, 'store_info', result[0])

				table_data['store_info']['id']['value'] = '1'

				ecommerce.display_form(table_data, 'store_info', 1, 'useValues', 1, db)
				
				ecommerce.alertsArea(form, "Store Info retrieved successfully");

		storeButtons('save')

		ecommerce.editHiddenFields(form["uHidden"].value, form["pHidden"].value)
		
		print "</FORM>"

		ecommerce.trailer(table_data, db)
		db.close()

		print "</BODY>"
		print "</HTML>"
		
	elif form["action"].value == "save":

		table_data = declarations.define_tables()

		print "<HTML>"
		print "<HEAD>"

		ecommerce.generate_form_javascript(table_data,'store_info','store_admin',0,0)

		ecommerce.title("Store Info Administration")

		print "</HEAD>" 

		ecommerce.bodySetup()

		ecommerce.mainHeading('Store Info Administration')

		ecommerce.subHeading('Edit Store Info')

		ecommerce.formSetup("store_admin","store_admin","return submitForm(document.store_admin)",declarations.store_info['db_name'])

		dbResult = ecommerce.connectDB(form["uHidden"].value, form["pHidden"].value,declarations.store_info['db_name'])

		if dbResult['status'] != 'success':

			 ecommerce.alertsArea(form,"Store Info could not be saved, could not connect to db" + dbResult['message'])

		else:

			db = dbResult['result']

			# save the Form
			dbResult = ecommerce.saveForm(table_data, db, None, "store_info", " WHERE id = '1'", form)

			# if the form was not successfully saved
			if dbResult['status'] != 'success':
				ecommerce.alertsArea(form,"Store Info could not be saved due to an error during save,\n" + dbResult['message'] )

			# form was successfully saved
			else:

				table_data = declarations.define_tables()
				table_data = ecommerce.formToTableData(table_data,'store_info', form)

				table_data['store_info']['id']['value'] = '1'

				ecommerce.display_form(table_data, 'store_info', 1, 'useValues', 1, db)
			
				ecommerce.alertsArea(form,"Store Info successfully saved")


		# generate function button row
		storeButtons('save')
			
		# generate hidden fields for form
		ecommerce.createHiddenFields(form["uHidden"].value, form["pHidden"].value)
			
		print "</FORM>"

		ecommerce.trailer(table_data, db)
		db.close()

		print "</BODY>"
		print "</HTML>"
			
else:

	edit_store_info(0)
