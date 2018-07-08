# $Id: view_properties.py,v 1.8 2000/04/07 02:24:35 davis Exp davis $
# Copyright (C) 1999 LinuXden, All Rights Reserved
# Copright Statement at http://www.linuxden.com/copyrighted_apps.html
# 
import os, string, sys
import cgi, glob
from pg import DB
import ecommerce
import declarations

ecommerce.htmlContentType()

def display_ad(table_data):
	
	print "<TABLE BORDER=0>"
	print "<TR><TD COLSPAN=5 ALIGN=CENTER>"

	ecommerce.image(
		image_name=table_data['properties']['image']['value'],
		store_name=declarations.store_info['db_name'])

	print "</TD></TR>"

	print "<TR>"
	print "<TR><TD COLSPAN=5 ALIGN=CENTER><HR></TD>"
	print "</TR>"
	
	print '<TR><TH><FONT FACE="Arial,Helvetica" SIZE="-1">Property Id</FONT></TH><TH><FONT FACE="Arial,Helvetica" SIZE="-1">Bedrooms</FONT></TH><TH><FONT FACE="Arial,Helvetica" SIZE="-1">Baths</FONT></TH><TH><FONT FACE="Arial,Helvetica" SIZE="-1">Square Footage</FONT></TH><TH><FONT FACE="Arial,Helvetica" SIZE="-1">Subdivision/Area</FONT></TH></TR>'	
	print "<TR>"

	ecommerce.tableColumn(table_data['properties']['id']['value'])
	ecommerce.tableColumn(table_data['properties']['bedrooms']['value'])
	ecommerce.tableColumn(table_data['properties']['baths']['value'])
	ecommerce.tableColumn(table_data['properties']['square_footage']['value'])
	ecommerce.tableColumn(table_data['properties']['subdivision']['value'])
	print "</TR>"

	print "<TR>"
	print "<TR><TD COLSPAN=5 ALIGN=CENTER><HR></TD>"
	print "</TR>"
	
	print '<TR><TH COLSPAN=5><FONT FACE="Arial,Helvetica" SIZE="-1">Description</FONT></TH></TR>'
	print "<TR>"
	print '<TD ALIGN=CENTER COLSPAN=5><FONT FACE="Arial,Helvetica" SIZE="-1">' + table_data['properties']['description']['value'] + "</FONT></TD>"
	print "</TR>"

	print "<TR>"
	print "<TR><TD COLSPAN=5 ALIGN=CENTER><HR></TD>"
	print "</TR>"

	print '<TR><TH><FONT FACE="Arial,Helvetica" SIZE="-1">Heating/Air</FONT></TH><TH><FONT FACE="Arial,Helvetica" SIZE="-1">Garage</FONT></TH><TH><FONT FACE="Arial,Helvetica" SIZE="-1">Date Built</FONT></TH><TH><FONT FACE="Arial,Helvetica" SIZE="-1">Electric Service</FONT></TH><TH><FONT FACE="Arial,Helvetica" SIZE="-1">School District</FONT></TH></TR>'
	print "<TR>"

	ecommerce.tableColumn(table_data['properties']['heating_air']['value'])
	ecommerce.tableColumn(table_data['properties']['car_garage']['value'])
	ecommerce.tableColumn(table_data['properties']['date_built']['value'])
	ecommerce.tableColumn(table_data['properties']['electric_service']['value'])
	ecommerce.tableColumn(table_data['properties']['school_district']['value'])
	print "</TR>"

	print "<TR>"
	print "<TR><TD COLSPAN=5 ALIGN=CENTER><HR></TD>"
	print "</TR>"

	print '<TR><TH><FONT FACE="Arial,Helvetica" SIZE="-1">Style</FONT></TH><TH><FONT FACE="Arial,Helvetica" SIZE="-1">Number of Rooms</FONT></TH><TH><FONT FACE="Arial,Helvetica" SIZE="-1">Acreage</FONT></TH><TH><FONT FACE="Arial,Helvetica" SIZE="-1">Full Basement</FONT></TH><TH><FONT FACE="Arial,Helvetica" SIZE="-1">Price</FONT></TH></TR>'
	print "<TR>"

	ecommerce.tableColumn(table_data['properties']['style']['value'])
	ecommerce.tableColumn(table_data['properties']['number_rooms']['value'])
	ecommerce.tableColumn(table_data['properties']['acreage']['value'])
	
	ecommerce.tableColumn(table_data['properties']['full_basement']['value'])

	if table_data['properties']['price']['value'] == '0.00':
		ecommerce.tableColumn('Not Listed')
	else:
		ecommerce.tableColumn('$ ' + table_data['properties']['price']['value'])
	
	print "</TR>"

	print "<TR>"
	print "<TR><TD COLSPAN=5 ALIGN=CENTER><HR></TD>"
	print "</TR>"

	print '<TR><TH><FONT FACE="Arial,Helvetica" SIZE="-1">Daytime Phone Number</FONT></TH><TH><FONT FACE="Arial,Helvetica" SIZE="-1">Evening Phone Number</FONT></TH><TH><FONT FACE="Arial,Helvetica" SIZE="-1">E-mail</FONT></TH><TH COLSPAN=2><FONT FACE="Arial,Helvetica" SIZE="-1">Directions</FONT></TH></TR>'
	print "<TR>"

	ecommerce.tableColumn(table_data['customers']['daytime_phone_number']['value'])
	ecommerce.tableColumn(table_data['customers']['evening_phone_number']['value'])

	print '<TD ALIGN=CENTER>'
	ecommerce.mailhref(table_data['customers']['email']['value'],table_data['customers']['email']['value'])
	print '</TD>'

	print '<TD ALIGN=CENTER COLSPAN=2><FONT FACE="Arial,Helvetica" SIZE="-1">' + table_data['properties']['directions']['value'] + "</FONT></TD>"
	print "</TR>"
	print "</TABLE>"

def query_properties(performDbQuery=0, onLoad=None, queryFields=None):

	table_data = declarations.define_tables()

	print "<HTML>"
	print "<HEAD>"

	ecommerce.javaScript("view_properties", 1)

	ecommerce.title("Property Listing")

	print "</HEAD>"

	ecommerce.bodySetup(onLoad)

	print '<CENTER>'
	print '<TABLE COLS=1 WIDTH=585>'
	print '<TR><TD>'

	ecommerce.mainHeading('Property Listing')

	ecommerce.subHeading('View Properties')

	ecommerce.formSetup("view_properties","view_properties","return submitForm(document.view_properties)",declarations.store_info['db_name'])

	if form.has_key("performDbQuery") or performDbQuery == 1:

		dbResult = ecommerce.connectDB(
			declarations.store_info['browser_username'],
			declarations.store_info['browser_password'],
			declarations.store_info['db_name'])
		
		# could not connect to db
		if dbResult['status'] != 'success':
			
			ecommerce.alertsArea(form, "Can not connect to database,\n" + dbResult['message'])
			
			# connected to db

			ecommerce.queryFunctionButtons(0, declarations.store_info['help_file'])

		else:
			db = dbResult['result']
			
			queryFields, whereFields = ecommerce.getQueryWhereFields(form, table_data, 'properties')

			if queryFields == None or queryFields == []:
				queryFields = []
				whereFields = None
				queryFields.append('town')
				queryFields.append('price')
				queryFields.append('square_footage')

			dbResult, queryStatement = ecommerce.executeQuery(db, 
													table_data, 
													'properties',
													queryFields, 
													whereFields, 
													'query', 
													ecommerce.viewPropertiesFunctionsHtml, 
													'ORDER BY id', 
													'id', 
													"display_property = 't'",
													['order_id', 'customer_id','display_property','image'])

			# if query was not successful
			if dbResult['status'] != 'success':
				ecommerce.alertsArea(form, "Could not retrieve properties from database,\n" + dbResult['message']);
			# else properties were retrieved ok
			else:
				ecommerce.alertsArea(form, "Last Query Statement: " + queryStatement + "\n" + `len(dbResult['result'])` + " properties retrieved from database");
				
			ecommerce.viewPropertiesFunctionButtons(declarations.store_info['help_file'])

	else:
		ecommerce.viewPropertiesFunctionButtons(declarations.store_info['help_file'])

	ecommerce.viewPropertiesHiddenFields(
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

	if form.has_key("performDbQuery") or performDbQuery == 1:
		return dbResult
	else:
		return {'status' : 'success', 'message' : 'query successful', 'result' : 0}

form = ecommerce.getFormData()

if form.has_key("action"):

	if form["action"].value == "query":

		query_properties(1)

	# view button pressed
	elif form["action"].value == "view":

		table_data = declarations.define_tables()

		print "<HTML>"
		print "<HEAD>"

		ecommerce.javaScript("view_properties")
		
		ecommerce.title("View Property Listing Id " + form['key_id'].value)

		print "</HEAD>" 

		ecommerce.bodySetup()

		ecommerce.mainHeading('Property Listing')
	
		ecommerce.subHeading('Property Ad: ' + form['key_id'].value)

		ecommerce.formSetup("view_properties","view_properties","return submitForm(document.view_properties)",declarations.store_info['db_name'])

		# attempt to connect to db
		dbResult = ecommerce.connectDB(form["uHidden"].value,form["pHidden"].value,declarations.store_info['db_name'])
		
		# if db connection failed
		if dbResult['status'] != 'success':

			# generate appropriate message in alerts area
			 ecommerce.alertsArea(form,"Property data could not be viewed, could not connect to db,\n" + dbResult['message'])			

		# else db connection succeeded
		else:

			# assign db connection variable
			db = dbResult['result']

			sqlStatement = "SELECT p.id, p.date_built, p.car_garage, p.town, p.subdivision, p.style, p.full_basement, p.bedrooms, p.baths, p.square_footage, c.daytime_phone_number, c.evening_phone_number, p.price, p.description, p.image, p.directions, c.email, p.heating_air, p.number_rooms, p.electric_service, p.school_district, p.acreage FROM properties p, customers c WHERE p.display_property = 't' AND p.id = '" + form["key_id"].value + "' AND p.customer_id = c.id" 

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
				table_data = ecommerce.dbToTableData(table_data, 'customers', result[0])

				display_ad(table_data)

		ecommerce.viewFunctionButtons('/' + declarations.store_info['db_name'] + '-cgi-bin/view_properties.pyc?username=' + form["uHidden"].value + '&password=' + form["pHidden"].value + '&performDbQuery=1', declarations.store_info['help_file'])

		print '</FORM>'

		ecommerce.trailer(table_data, db)
		db.close()

		print "</BODY>"
		print "</HTML>"

else:

	query_properties(1)
