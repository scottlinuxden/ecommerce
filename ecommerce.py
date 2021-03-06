# $Id: ecommerce.py,v 1.9 2000/04/09 22:19:56 davis Exp davis $
# Copyright (C) 1999 LinuXden, All Rights Reserved
# Copright Statement at http://www.linuxden.com/copyrighted_apps.html
#
import os, string, sys
import cgi, glob
import types
from pg import DB
import _pg
import types
import StringIO, smtplib

def send_email(mailserver, from_address, recipients, subject, content):

	recipient_list = ''
	for i in recipients:
		recipient_list = recipient_list + ', '

	recipient_list = recipient_list[:-2]
	
	out=StringIO.StringIO()
	out.write("Subject: %s\n" % subject)
	out.write("To: %s\n\n" % recipient_list)
	out.write(content)

	mail=smtplib.SMTP(mailserver)

	mail.sendmail(
		from_addr=from_address,
		to_addrs=recipients,
		msg=out.getvalue())

"""
Global definitions for this module
queryResult ->
	{'status' : [error|success], 'message' : string, 'result' : [rows returned by query|None]}
"""

def sort(list, field):
	res = []
	for x in list:
		i = 0
		for y in res:
			if x[field] <= y[field]: break
			i = i + 1
		res[i:i] = [x]
	return res

def mainHeading(topic):
	"""
	Generates the Main Header HTML
	"""
	print '<FONT FACE="Arial,Helvetica" SIZE="-1" COLOR="darkRed"><B>' + topic + '</B></FONT><BR>'

def subHeading(topic):
	"""
	Generates a Sub Heading HTML
	"""
	print '<FONT FACE="Arial,Helvetica" SIZE="-1" COLOR="blue"><B><i>' + topic + '</i></B></FONT><BR>'

def printText(text,color='blue'):
	"""
	Prints all text in a specified font
	"""
	print '<FONT FACE="Arial,Helvetica" SIZE="-1" COLOR="' + color + '">' + text + '</FONT><BR>'

def bodySetup(onLoad=None,bgColor='#B7BAB7',textColor='#000000'):
	"""
	Generates the BODY tag for an HTML page with the optional onLoad specifier
	to execute a JavaScript function when the page loads
	"""
	print '<BODY BGCOLOR="' + bgColor + '" TEXT="' + textColor + '"'
	if onLoad != None:
		print ' onLoad="' + onLoad + '"'
	print '>'

def buildColumnDeclaration(table_name, column_name, table_data):
	"""
	Builds a column declaration to be used in a create table statement
	"""
	sqlStatement = column_name + " "
	
	if (table_data[table_name][column_name]["type"] == 'VARCHAR') or (table_data[table_name][column_name]["type"] == 'DECIMAL'):
		
		sqlStatement = sqlStatement + table_data[table_name][column_name]["type"] + "(" + table_data[table_name][column_name]["db_size"] + ")"
		
	else:
		sqlStatement = sqlStatement + table_data[table_name][column_name]["type"]
		
	if table_data[table_name][column_name]["default"] != None:
			
		if (table_data[table_name][column_name]["type"] == 'VARCHAR') or \
		   (table_data[table_name][column_name]["type"] == 'DECIMAL') or \
		   (table_data[table_name][column_name]["type"] == 'BOOL'):
				
			sqlStatement = sqlStatement + " DEFAULT '" + table_data[table_name][column_name]["default"] + "'" 
				
		else:
			sqlStatement = sqlStatement + " DEFAULT " + table_data[table_name][column_name]["default"]
				
	if column_name == 'id':
		sqlStatement = sqlStatement + " NOT NULL UNIQUE PRIMARY KEY"

	return sqlStatement

def saveForm(table_data, db, key, table_name, where_clause, form, echoStatement=0, fromForm=1,insert_regardless=0):
	"""
	Will save field data in form or table_data which is designated by the
	fromForm argument which if it is 0 the save is performed from table_data
	else if it is 1 the save is done from form.  That has the same names of 
	the fields in
	table_name found in table_data.  The where_clause specifies what rows 
	should be updated or if row does not exist an insert is performed on table.
	if echoStatement == 1 then the sql statement that is performed for the
	save of the form data is echoed to standard output.  The db argument is
	an already open database connection.  The key argument is the database key
	or id that is used for an insert should the row not already exist.  If
	any of the form fields are numeric fields and the field value is blank
	then the blank field value is converted to int4 -> 0, float4 -> 0.0, 
	decimal -> 0.00 in order to be saved to the database.
	the result of the save is returned as a queryResult dictionary value, see
	top of file for return type
	"""

	if fromForm:
		keyitems = form.keys()
	else:
		keyitems = table_data[table_name].keys()

	if not insert_regardless:
		sqlStatement = "SELECT count(*) FROM " + table_name + " " + where_clause

		queryResult = executeSQL(db, sqlStatement)
	
		result = queryResult['result']

		rows_which_match = result[0]["count"]

	else:
		rows_which_match = 0

	if rows_which_match > 0:

		# row exists perform an update of data
		sqlStatement = "UPDATE " + table_name + " SET " 

		for i in keyitems:

			if table_data[table_name].has_key(i):

				sqlStatement = sqlStatement + i + " = "

				# if the type of the field is varchar, date, or boolean
				if (table_data[table_name][i]["type"] == 'VARCHAR') or (table_data[table_name][i]["type"] == 'DATE') or (table_data[table_name][i]["type"] == 'BOOL'):

					# if the field is a boolean
					if table_data[table_name][i]["type"] == 'BOOL':

						if fromForm:
							if string.lower(form[i].value) == 'yes':
								sqlStatement = sqlStatement + "'t', "
							elif string.lower(form[i].value) == 'no':
								sqlStatement = sqlStatement + "'f', "
						else:

							if string.lower(table_data[table_name][i]['value']) == 'yes':
								sqlStatement = sqlStatement + "'t', "
							elif string.lower(table_data[table_name][i]['value']) == 'no':
								sqlStatement = sqlStatement + "'f', "

					# else field is not a boolean field
					else:

						if fromForm:
							if string.strip(form[i].value) == '':
								sqlStatement = sqlStatement + "NULL, "
							else:
								sqlStatement = sqlStatement + "'" + form[i].value + "', "

						else:
							if string.strip(table_data[table_name][i]['value']) == '':
								sqlStatement = sqlStatement + "NULL, "
							else:
								sqlStatement = sqlStatement + "'" + table_data[table_name][i]['value'] + "', "

				# else field is not a varchar, boolean, or date
				else:

					if fromForm:
						if string.strip(form[i].value) == '':
							sqlStatement = sqlStatement + "NULL, "
						else:
							sqlStatement = sqlStatement + form[i].value + ", "
							
					else:
						if string.strip(table_data[table_name][i]['value']) == '':
							sqlStatement = sqlStatement + "NULL, "
						else:
							sqlStatement = sqlStatement + table_data[table_name][i]['value'] + ", "

		# remove last comma
		sqlStatement = sqlStatement[:-2]

		if where_clause != None:
			sqlStatement = sqlStatement + where_clause
		
	else:

		# row does not exist so insert
		sqlStatement = "INSERT INTO " + table_name + " ("

		if key != None and fromForm == 1:
			sqlStatement = sqlStatement + "id, "

		for i in keyitems:

			if table_data[table_name].has_key(i):

				sqlStatement = sqlStatement + i + ", "

		sqlStatement = sqlStatement[:-2] + ") VALUES ("

		if key != None and fromForm == 1:
			sqlStatement = sqlStatement + "'" + key + "', "

		for i in keyitems:

			if table_data[table_name].has_key(i):

				if (table_data[table_name][i]["type"] == 'VARCHAR') or (table_data[table_name][i]["type"] == 'DATE') or (table_data[table_name][i]["type"] == 'BOOL'):

					if table_data[table_name][i]["type"] == 'BOOL':

						if fromForm:
							if string.lower(form[i].value) == 'yes':
								sqlStatement = sqlStatement + "'t', "
							elif string.lower(form[i].value) == 'no':
								sqlStatement = sqlStatement + "'f', "
						else:
							if string.lower(table_data[table_name][i]['value']) == 'yes':
								sqlStatement = sqlStatement + "'t', "
							elif string.lower(table_data[table_name][i]['value']) == 'no':
								sqlStatement = sqlStatement + "'f', "
					else:

						if fromForm:
							if string.strip(form[i].value) == '':
								sqlStatement = sqlStatement + "NULL, "
							else:
								sqlStatement = sqlStatement + "'" + form[i].value + "', "
						else:
							if string.strip(table_data[table_name][i]['value']) == '':
								sqlStatement = sqlStatement + "NULL, "
							else:
								sqlStatement = sqlStatement + "'" + table_data[table_name][i]['value'] + "', "
								

				else:

					if fromForm:
						if string.strip(form[i].value) == '':
							sqlStatement = sqlStatement + "NULL, "
						else:
							sqlStatement = sqlStatement + form[i].value + ", "
							
					else:
						if string.strip(table_data[table_name][i]['value']) == '':
							sqlStatement = sqlStatement + "NULL, "
						else:
							sqlStatement = sqlStatement + table_data[table_name][i]['value'] + ", "

		# remove last comma
		sqlStatement = sqlStatement[:-2] + ")"

	if echoStatement == 1:
		print "\nSQL Statement:\n" + sqlStatement + "\nPerformed successfully"

	queryResult = executeSQL(db, sqlStatement)

	return queryResult

def textbox(table_name, name, value, size, maxlength, leaveFocus, gainFocus, inputType='text'):
	""" 
	Generates HTML for a form password, hidden, or text field.  Table Name is
	reserved for future use. name is the name of the field, value is the value
	to set the field to, size is the size to initially display the field with
	and maxlength is the maximum length the field can scroll.  leavefocus is
	the javascript function to call when the operator moves out of the field.
	gainFocus is the javascript function to call when the operator moves into
	the field.  inputType of field can be password, hidden, or text
	HTML is written to standard output.
	"""
	if type(value) is types.IntType:
		valueItem = `value`
	elif type(value) is types.FloatType:
		valueItem = `value`
	elif type(value) is types.LongType:
		valueItem = `value`
	elif type(value) is types.StringType:
		valueItem = value

	valueItem = string.strip(valueItem)

	print '<INPUT NAME="' + name + '" TYPE="' + inputType + '" VALUE="' + valueItem + '"'

	print ' SIZE="' + size + '" MAXLENGTH="' + maxlength + '"', 

	if leaveFocus != None:
		print ' onBlur="' + leaveFocus + '"',

	if gainFocus != None:
		print ' onFocus="' + gainFocus + '"',
	
	print '>'

def optionMenu(name, size, options, selected):
	"""
	Generates HTML for an optionMenu form item that can allow 1-many
	selections from its options provided.
	name is the name of the optionMenu
	size is the number of items to display at a time
	options is a list sequence of all valid options that the menu 
	should display
	selected is a list sequence which is a one-to-one mapping to 
	the options list which contains per option specified by the options list
	either a NULL or blank string if the option should not be selected when
	displayed or the keyword SELECTED if the option should be selected
	HTML is written to standard output
	"""
	print '<FONT FACE="Arial,Helvetica" SIZE="-1">'
	print '<SELECT NAME="' + name + '" SIZE=' + size + '>\n'
	for i in range(0,len(options)):
		print '<OPTION ' + selected[i] + '>' + options[i] + '\n'
	print '</SELECT>'
	print '</FONT>'

def textarea(table_name, name, value, rows, cols, leaveFocus, gainFocus):
	"""
	Generates HTML for a form textarea field
	table_name is reserved for future use and should contain the table name
	that the field maps to
	name is the name of the textarea form item
	value is the value to set the textarea field to
	rows is the number of rows for the initial size of the textarea
	cols is the number of cols to display at a time
	leaveFocus is the javascript handler to call when operator leaves field
	gainFocus is the javascript handler to call when operator enters field
	HTML generated is written to standard output.
	"""

	print '<TEXTAREA NAME="' + name + '" ROWS="' + rows + '" COLS="' + cols + '" SIZE="' + rows + "," + cols + '" WRAP="virtual" ',

	if leaveFocus != None:
		print ' onBlur="' + leaveFocus + '"',
	if gainFocus != None:
		print ' onFocus="' + gainFocus + '"',

	print '>'

	if type(value) is types.IntType:
		valueItem = `value`
	elif type(value) is types.FloatType:
		valueItem = `value`
	elif type(value) is types.LongType:
		valueItem = `value`
	elif type(value) is types.StringType:
		valueItem = value

	valueItem = string.strip(valueItem)

	print valueItem + '</TEXTAREA>'

def urlhref(target, link):
	"""
	Generates HTML for a selectable link than when selected visits the target
	specified
	target is the url of the web page to visit when link clicked
	link is the text to be displayed for the link.  HTML is written to standard
	output
	"""
	print '<A HREF="' + target + '">' + link + '</A>'

def mailhref(target, link, subject_line=None):
	"""
	Generates HTML for a mail link where
	target is the e-mail address of the recipient of the message
	link is the text of the link to be displayed
	subject_line is the Subject of the message to be pre-filled when
	mail browser appears.  HTML is written to standard output.
	"""
	if subject_line == None:
		print '<A HREF="mailto:' + target + '">' + link + '</A>'
	else:
		print '<A HREF="mailto:' + target + '?Subject=' + subject_line + '">' + link + '</A>'
		
def image(image_name, store_name, target=None, imageMissing='imageMissing.gif', hSize=None, vSize=None):
	"""
	Generates HTML for an image that should be placed in the images script
	alias directory for your web server, on Linux /home/httpd/images.  HTML
	is written to standard output.
	"""
	if string.strip(image_name) != "" and \
	   os.path.exists(os.path.join("/home",store_name,'images',image_name)):
		image_name = string.strip(image_name)
	else:
		image_name = 'imageMissing.gif'

	if target == None:
		target = '/' + store_name + '-images'
		
	print '<IMG SRC="' + target + '/' + image_name + '">'

def trailer(table_data, db, copyright_date='1999'):
	"""
	Generates HTML for a trailer message describing Copyright and e-commerce
	links for LinuXden.  HTML is written to standard output.
	"""

	sqlStatement = selectAllColumnsSqlStatement(table_data,'store_info','1')
		
	dbResult = executeSQL(db, sqlStatement)
		
	if dbResult['status'] != 'success':
		
		return 'error'

	else:
			
		result = dbResult['result']
		
		table_data = dbToTableData(table_data, 'store_info', result[0])
		
		print '<P ALIGN=RIGHT><FONT FACE="Arial,Helvetica" SIZE="-2" COLOR="BLACK">'
		print table_data['store_info']['name']['value'] + '<BR>'
		print table_data['store_info']['address_line_1']['value'] + '<BR>'

		if string.strip(table_data['store_info']['address_line_2']['value']) != '':
			print table_data['store_info']['address_line_2']['value'] + '<BR>'

		print table_data['store_info']['city']['value'] + ', ' + table_data['store_info']['state']['value'] + '&nbsp;&nbsp;' + table_data['store_info']['zip']['value'] + '<BR>'
		if string.strip(table_data['store_info']['phone_number_voice']['value']) != '':
			print 'Voice: '  + table_data['store_info']['phone_number_voice']['value'] + '<BR>'

		if string.strip(table_data['store_info']['phone_number_fax']['value']) != '':
			print 'FAX: ' + table_data['store_info']['phone_number_fax']['value'] + '<BR>'

		if string.strip(table_data['store_info']['email']['value']) != '':
			print 'E-mail: <A HREF="mailto:' + table_data['store_info']['email']['value'] + '">' + table_data['store_info']['email']['value'] + '</A><BR>'

		print '<BR><BR><FONT FACE="Arial,Helvetica" SIZE="-2" COLOR="BLACK">Copyright &copy;'+ copyright_date + '<BR>'
		print 'All Rights Reserved<BR>Powered by <A HREF="http://www.linuxden.com/commerce.html">XdenCommerce</A></FONT>'

def usernamePasswordDisplay(username, password):
	"""
	Generate a username and password display fields for a form and 
	authentication.  HTML is written to standard output.
	"""
	print '<TABLE><BORDER=0>'
	print '<TR>'

	tableColumn('<B>Username:</B>')
	print '<TD ALIGN=CENTER NOWRAP>'

	textbox(None,'username',username,'9','9',"checkBlankField(this, 'Username')","displayHint('Enter your username')")
	print '</TD>'

	tableColumn('<B>Password:</B>')

	print '<TD ALIGN=CENTER NOWRAP>'
	textbox(None,'password',password,'8','8',"checkBlankField(this, 'Password')","displayHint('Enter your password')",'password')
	print '</TD>'
	print '</TR>'
	print '</TABLE>'

def formSetup(name, cgi_name, submit_action, store_name, enc_type='application/x-www-form-urlencoded'):
	"""
	Generates HTML for the description of a form to follow
	name is the name of the form
	cgi_name is the name of the cgi to execute to process form
	submit_action is a javascript function to execute prior to form 
	processing by cgi.  HTML is written to standard output
	"""
	print '<FORM NAME="' + name + '" ACTION="/' + store_name + '-cgi-bin/' + cgi_name + '.pyc"'
	if submit_action != None:
		print ' onSubmit="' + submit_action + '"'

	print ' METHOD="POST" ENCTYPE="' + enc_type + '">'  

def generate_form_javascript(table_data,table_name,form_name,firstErrorDontSubmit=0,assign_hidden_authentication=0):
	''' 
	 Generates a series of javascript form processing support
	 functions.  Also generates a validate_form javascript function
	 which will call all validation routines listed for each field in
	 the table specified by table which is found in the table_data
	 declarations.  When the submit form action is processed this
	 routine is called as long as <form action="return
	 validate_form()"> is specified in the HTML.  All validation
	 routines called by validate_form should perform all validation
	 responses to errors such as display an alert window, etc.  This
	 routine merely generates a dynamically built javascript procedure
	 to verify all fields which should be verified before a form is
	 sent to http server.  All arguments to validation routines can
	 either be string or numeric.  If the argument is string it is
	 surrounded by single quotes and syntax generated to preserve
	 white space in the string.  Numerics are not converted to strings
	 before the syntax is emitted to the validate_form function so if
	 you need all arguments to the javascript to be string then
	 convert the numeric to a string representation.  The
	 firstErrorDontSubmit parameter when set to the default of 0
	 signifies to continue validation through the entire list even if
	 fields have errors.  This could possibly display multiple error
	 message, etc. if the validation routines perform this operation.
	 When set to 1 signifies that validation should cease on the first
	 error.
	'''

	form_routine = {}
	print '<SCRIPT>'

	form_routine['displayHint'] = {'number_arguments' : 1}
	print "  function displayHint(hint) {"
	print "	top.status = hint;"
	print "	return true;"
	print "  }\n"

	form_routine['goto_url'] = {'number_arguments' : 1}
	print "function goto_url(url) {"
	print "  window.location.href = url;"
	print "  return true;"
	print "}\n"

	form_routine['confirmDialog'] = {'number_arguments' : 1}
	print 'function confirmDialog(message) {'
	print '	if (window.confirm(message)) {'
	print "	  return true;"
	print "	}"
	print "	else {"
	print "	  return false;"
	print "	}"
	print '}\n'

	form_routine['previousUrl'] = {'number_arguments' : 1}
	print '  function previousUrl(url) {'
	print '	top.history.go(url);'
	print '	return true;'
	print '  }\n'


	form_routine['execute'] = {'number_arguments' : 2}
	print "function execute(action_name, id_key) {"
	print "  var status = false;"
	print '  document.' + form_name + '.action.value = action_name;'
	print '  document.' + form_name + '.key_id.value = id_key;'
	print '  status = submitForm(' + 'document.' + form_name +');'
	print '  if (status == true) {'
 
	if assign_hidden_authentication == 1:
		print '	document.' + form_name + '.uHidden.value = document.' + form_name + '.username.value;'
		print '	document.' + form_name + '.pHidden.value = document.' + form_name + '.password.value;'

	print '	document.' + form_name + '.submit();'
	print '	return true;'
	print '  }'
	print '  else {'
	print "	return false;"
	print '  }'
	print "}\n"

	form_routine['process_item'] = {'number_arguments' : 3}
	print "function process_item(action_name, item_no, form_key) {"
	print "  var status = false;"
	print '  document.' + form_name + '.action.value = action_name;'
	print '  document.' + form_name + '.key_id.value = form_key;'
	print '  document.' + form_name + '.item_no.value = item_no;'
	print '  status = submitForm(' + 'document.' + form_name +');'
	print '  if (status == true) {'
 
	if assign_hidden_authentication == 1:
		print '	document.' + form_name + '.uHidden.value = document.' + form_name + '.username.value;'
		print '	document.' + form_name + '.pHidden.value = document.' + form_name + '.password.value;'

	print '	document.' + form_name + '.submit();'
	print '	return true;'
	print '  }'
	print '  else {'
	print "	return false;"
	print '  }'
	print "}\n"
 
	form_routine['checkBlankField'] = {'number_arguments' : 2}
	print "  function checkBlankField(field,label) {"
	print "	var str = field.value;"
	print "	var blankStr = true;"
	print "	var temp_str = \"\""
	
	print "	for (var i = 0; i < str.length; i++) {"
	print "	  var ch = str.substring(i,i+1)"
	print "	  if (ch != \" \") {"
	print "		blankStr = false;"
	print "		break;"
	print "	  }"
	print "	}"
	
	print "	if (blankStr || str.length == 0) {"
	print "	  alert_window(label,'Field can not be blank',field.value,'Field is required');"
	print "	  return false;"
	print "	}"
	print "	else {"
	print "	  return true;"
	print "	}"
	print "  }\n"

	form_routine['checkLength'] = {'number_arguments' : 3}
	print "  function checkLength (textarea, maxlength, label) {"
	print "	if (textarea.value.length > maxlength) {"
	print "	  alert_window(label,'Length of ' + label + ' exceeds maximum length of ' + maxlength,'Please specify less characters','Length should be: ' + maxlength);"
	print "	  return false;"
	print "	}"
	print "	return true;"
	print "  }\n"
  
	form_routine['daysInMonth'] = {'number_arguments' : 2}
	print '  function daysInMonth(month, year) {'
	print '	var months = "312831303130313130313031";'
	print '	if (month == 2) {'
	print '	  if (((year % 4) == 0) && ((year % 100 != 0) || ((year % 400) == 0))) {'
	print '		months = months.substring(0,2) + "29" + months.substring(4,24);'
	print '	  }'
	print '	}'
	print '	return months.substring((month-1)*2,((month-1)*2)+2);'
	print '  }\n'

	form_routine['valid_integer'] = {'number_arguments' : 4}
	print '  function valid_integer(number,format,label,required) {'
	print '	if ((required) && (number.value.length) == 0) {'
	print '	  alert_window(label,"Integer value required","No integer input provided",format);'
	print '	  return false;'
	print '	}'

	print '	if ((!required) && (number.value.length == 0)) {'
	print '	  return true;'
	print '	}'

	print '	if (format.length != 0) {'
	print '	  if (number.value.length != format.length) {'
	print '		alert_window(label,"Invalid integer specified","Number digits input does not match format",format);'
	print '		return false;'
	print '	  }'
	print '	}'
	
	print '	for (var i = 0; i < number.value.length; i++) {'
	print '	  if (!is_digit(number.value.substring(i,i+1))) {'
	print '		alert_window(label,"Invalid integer specified","All digits must be 0-9",format);'
	print '		return false;'
	print '	  }'
	print '	}'
	print '	return true;'
	print '  }\n'

	form_routine['valid_float'] = {'number_arguments' : 4}
	print '  function valid_float(number,format,label,required) {'

	print '	var num_periods = 0;'
	print '	var dec_pos = 0;'

	print '	if ((required) && (number.value.length) == 0) {'
	print '	  alert_window(label,"Float value required","No floating input provided",format);'
	print '	  return false;'
	print '	}'

	print '	if ((!required) && (number.value.length == 0)) {'
	print '	  return true;'
	print '	}'

	print '	if (format.length != 0) {'
	print '	  if (number.value.length != format.length) {'
	print '		 alert_window(label,"Invalid float specified","Number digits input does not match format",format);'
	print '		 return false;'
	print '	  }'

	print '	  for (var i = 0; i < number.value.length; i++) {'

	print "		if (format.substring(i,i+1) == '.') {"
	print "		  if (number.value.substring(i,i+1) != '.') {"
	print '			alert_window(label,"Invalid float specified","Number specified does not match format",format);'
	print '			return false;'
	print '		  }'
	print '		}'

	print "		else if (format.substring(i,i+1) == '#') {"
	print '		  if (!is_digit(number.value.substring(i,i+1))) {'
	print '			alert_window(label,"Invalid float specified","Number specified does not match format",format);'
	print '			return false;'
	print '		  }'			  
	print '		}'
	print '	  }'
	print '	  return true;'
	print '	}'
	print '	else {'
	print '	  for (var i = 0; i < number.value.length; i++) {'
	print "		if (number.value.substring(i,i+1) == '.') {"
	print '		  dec_pos = i;'
	print '		  num_periods = num_periods + 1;'
	print '		}'
	print '		else if (!is_digit(number.value.substring(i,i+1))) {'
	print "		  alert_window(label,'Invalid float specified','Non-digit found in float specified','9.9');"
	print '		  return false;'
	print '		}'
	print '	  }'

	print '	  if (num_periods != 1) {'
	print '		alert_window(label,"Invalid float specified","Number specified should have one decimal point","9.9");'
	print '		return false;'
	print '	  }'
	print '	  else {'
	print '		if (dec_pos == 0) {'
	print '		  alert_window(label,"Invalid float specified","Number specified should have a leading digit before decimal","9.9");'
	print '		  return false;'
	print '		}'
	print '		if (dec_pos == number.value.length) {'
	print '		  alert_window(label,"Invalid float specified","Number specified should have a trailing digit after decimal","9.9");'
	print '		  return false;'
	print '		}'
	print '	  }'
	print '	}'
	print '  }\n'

	form_routine['valid_money'] = {'number_arguments' : 4}
	print '  function valid_money(number,format,label,required) {'

	print '	var num_periods = 0;'
	print '	var dec_pos = 0;'

	print '	if ((required) && (number.value.length) == 0) {'
	print '	  alert_window(label,"Dollar amount value required","No dollar amount provided",format);'
	print '	  return false;'
	print '	}'

	print '	if ((!required) && (number.value.length == 0)) {'
	print '	  return true;'
	print '	}'

	print '	if (format.length != 0) {'
	print '	  if (number.value.length != format.length) {'
	print '		 alert_window(label,"Invalid dollar amount specified","Number digits input does not match format",format);'
	print '		 return false;'
	print '	  }'

	print '	  for (var i = 0; i < number.value.length; i++) {'

	print "		if (format.substring(i,i+1) == '.') {"
	print "		  if (number.value.substring(i,i+1) != '.') {"
	print '			alert_window(label,"Invalid dollar amount specified","Number specified does not match format",format);'
	print '			return false;'
	print '		  }'
	print '		}'

	print "		else if (format.substring(i,i+1) == '#') {"
	print '		  if (!is_digit(number.value.substring(i,i+1))) {'
	print '			alert_window(label,"Invalid dollar amount specified","Number specified does not match format",format);'
	print '			return false;'
	print '		  }'			  
	print '		}'
	print '	  }'
	print '	  return true;'
	print '	}'
	print '	else {'
	print '	  for (var i = 0; i < number.value.length; i++) {'
	print "		if (number.value.substring(i,i+1) == '.') {"
	print '		  dec_pos = i;'
	print '		  num_periods = num_periods + 1;'
	print '		}'
	print '		else if (!is_digit(number.value.substring(i,i+1))) {'
	print "		  alert_window(label,'Invalid dollar amount specified','Non-digit found in dollar amount specified','9.99');"
	print '		  return false;'
	print '		}'
	print '	  }'

	print '	  if (num_periods != 1) {'
	print '		alert_window(label,"Invalid dollar amount specified","Number specified should have one decimal point","9.99");'
	print '		return false;'
	print '	  }'
	print '	  else {'
	print '		if (dec_pos == 0) {'
	print '		  alert_window(label,"Invalid dollar amount specified","Number specified should have a leading digit before decimal","9.99");'
	print '		  return false;'
	print '		}'
	print '		if ((dec_pos + 3) != number.value.length) {'
	print '		  alert_window(label,"Invalid dollar amount specified","Number specified should have 2 trailing digits after decimal","9.99");'
	print '		  return false;'
	print '		}'
	print '	  }'
	print '	  return true;'
	print '	}'
	print '  }\n'

	form_routine['valid_format'] = {'number_arguments' : 4}
	print '  function valid_format(field,format,label,required) {'
	print '	if ((required) && (field.value.length) == 0) {'
	print '	  alert_window(label,"Input value required","No input provided",format);'
	print '	  return false;'
	print '	}'

	print '	if ((!required) && (field.value.length == 0)) {'
	print '	  return true;'
	print '	}'

	print '	if (field.value.length != format.length) {'
	print '	  alert_window(label,"Not enough input provided","Data entered does not match format",format);'
	print '	  return false;'
	print '	}'

	print '	for (var i = 0; i < field.value.length; i++) {'
	print "	  if (format.substring(i,i+1) == '#') {"
	print '		if (!is_digit(field.value.substring(i,i+1))) {'
	print '		  alert_window(label,"Invalid character specified","Character specified: " + field.value.substring(i,i+1) + " does not match format",format);'
	print '		  return false;'
	print '		}'			  
	print '	  }'
	print "	  else if (format.substring(i,i+1) == 'L') {"
	print '		if (!is_letter(field.value.substring(i,i+1))) {'
	print '		  alert_window(label,"Invalid character specified","Character specified: " + field.value.substring(i,i+1) + " does not match format",format);'
	print '		  return false;'			
	print '		}'
	print '	  }'
	print "	  else if ((format.substring(i,i+1) != '*') && (format.substring(i,i+1) != field.value.substring(i,i+1))) {"
	print '		  alert_window(label,"Invalid character specified","Character specified: " + field.value.substring(i,i+1) + " does not match format",format);'
	print '		  return false;			'
	print '	  }'
	print '	}'
	print '	return true;'
	print '  }\n'

	form_routine['alert_window'] = {'number_arguments' : 4}
	print '  function alert_window(field_name, message, erroneous_data, format) {'
	print "	window.alert('Field Name: ' + field_name + '\\n' + message + ': ' + erroneous_data + '\\n' + 'Format: ' + format);"
	print '	return true;'
	print '  }\n'

	form_routine['is_digit'] = {'number_arguments' : 1}
	print '  function is_digit(character) {'
	print "	if (character < '0' || character > '9') {"
	print '	  return false;'
	print '	}'
	print '	else {'
	print '	  return true;'
	print '	}'
	print '  }\n'

	form_routine['is_letter'] = {'number_arguments' : 1}
	print '  function is_letter(character) {'
	print "	if ((character > 'a' && character < 'z') || (character > 'A' && character < 'Z')) {"
	print '	  return true;'
	print '	}'
	print '	else {'
	print '	  return false;'
	print '	}'
	print '  }\n'

	form_routine['valid_date'] = {'number_arguments' : 3}
	print '  function valid_date(date_time,label,required) {'

	print '	if ((required) && (date_time.value.length == 0)) {'
	print '	  alert_window(label,"Date value required","No date input provided","MM-DD-YYYY");'
	print '	  return false;'
	print '	}'

	print '	if ((!required) && (date_time.value.length == 0)) {'
	print '	  return true;'
	print '	}'

	print '	if (date_time.value.length != 10) {'
	print "	   alert_window(label,'Invalid date specified',date_time.value + ' is not long enough','MM-DD-YYYY');"
	print '	   return false;'
	print '	}'

	print '	for (var i = 0; i < 2; i++) {'
	print '	  var ch = date_time.value.substring(i,i+1);'
	print '	  if (!is_digit(ch)) {'

	print "	   alert_window(label,'Invalid month specified',date_time.value.substring(0,2) + ' is not 01-12','MM-DD-YYYY');"

	print '		return false;'
	print '	  }'
	print '	}'

	print '	if (date_time.value.substring(0,2) <= 0 || date_time.value.substring(0,2) > 12) {'

	print "	  alert_window(label,'Invalid month specified',date_time.value.substring(0,2) + ' is not 01-12','MM-DD-YYYY');"

	print '	  return false;'
	print '	}'

	print "	if (date_time.value.substring(2,3) != '-') {"

	print "	  alert_window(label,'Invalid month/day delimiter specified',date_time.value.substring(2,3) + ' is not -','MM-DD-YYYY');"

	print '	  return false;'
	print '	}'

	print '	for (var i = 3; i < 5; i++) {'
	print '	  var ch = date_time.value.substring(i,i+1);'
	print '	  if (!is_digit(ch)) {'

	print "		alert_window(label,'Invalid day specified',date_time.value.substring(3,5) + ' is not 01-31','MM-DD-YYYY');"

	print '		return false;'
	print '	  }' 
	print '	}'

	print '	if (date_time.value.substring(3,5) <= 0 || date_time.value.substring(3,5) > 31) {'

	print "	  alert_window(label,'Invalid day specified',date_time.value.substring(3,5) + ' is not 01-31','MM-DD-YYYY');"

	print '	  return false;'
	print '	}'

	print '	if (date_time.value.substring(3,5) > daysInMonth(date_time.value.substring(0,2), date_time.value.substring(6,10))) {'

	print "	  alert_window(label,'Invalid day specified',date_time.value.substring(3,5) + ' is not 01-' + daysInMonth(date_time.value.substring(0,2),date_time.value.substring(6,10)),'MM-DD-YYYY');"

	print '	  return false;'
	print '	}'

	print "	if (date_time.value.substring(5,6) != '-') {"

	print "	  alert_window(label,'Invalid day/year delimiter specified',date_time.value.substring(5,6) + ' is not -','MM-DD-YYYY');"

	print '	  return false;'
	print '	}'

	print '	for (var i = 6; i < 10; i++) {'
	print '	  var ch = date_time.value.substring(i,i+1);'

	print '	  if (!is_digit(ch)) {'

	print "		alert_window(label,'Invalid year specified',date_time.value.substring(6,10) + ' is not in range 1800-2037','MM-DD-YYYY');"

	print '		return false;'
	print '	  }' 
	print '	}'

	print '	if (date_time.value.substring(6,10) < 1800 || date_time.value.substring(6,10) > 2037) {'
	print "	  alert_window(label,'Invalid year specified',date_time.value.substring(6,10) + ' is not in range 1800-2037','MM-DD-YYYY');"
	print '	  return false;'
	print '	}'
	print '	return true;'
	print '  }\n'

	validationRoutineFound = 0

	# process all fields in field list
	for field_name in table_data[table_name].keys():

		# if the table declaration has a validation routine for the item in the
		# field list being processed
		if table_data[table_name][field_name].has_key('validation_routine') and table_data[table_name][field_name]['validation_routine'] != None:

			# if the field is not currently being displayed on form or is being displayed but not editable 
			if table_data[table_name][field_name]['display'] != 'editable' or \
			   table_data[table_name][field_name]['display'] == 'Hidden':
				# skip this field no validation required since it is not displayed or field designated
				# as not editable
				continue

			if table_data[table_name][field_name]['validation_routine'] not in form_routine.keys():
				raise Invalid_Form_Routine

			if len(table_data[table_name][field_name]['validation_arguments']) != form_routine[table_data[table_name][field_name]['validation_routine']]['number_arguments']:
				raise Invalid_Num_Args_For_Form_Routine

			if not validationRoutineFound:
				print '  function validate_form(form) {'
				print '	var error_in_form = false;'
				validationRoutineFound = 1

			# emit the if statement using the routine name and arguments specified
			# by field list

			print '	if (' + table_data[table_name][field_name]['validation_routine'] + '(',

			# if the validation routine has arguments
			if table_data[table_name][field_name]['validation_arguments'] != None:

				for argument_number in xrange(0,len(table_data[table_name][field_name]['validation_arguments'])):
					if argument_number != 0:
						print ','
					if type(table_data[table_name][field_name]['validation_arguments'][argument_number]) is types.StringType:
						print table_data[table_name][field_name]['validation_arguments'][argument_number],
					elif type(table_data[table_name][field_name]['validation_arguments'][argument_number]) is types.IntType or type(table_data[table_name][field_name]['validation_arguments'][argument_number]) is types.FloatType:
						print `table_data[table_name][field_name]['validation_arguments'][argument_number]`,

			print ') == false) {'
			if firstErrorDontSubmit:
				print '	  return false;'
			else:
				print '	  error_in_form = true;'
			print '	}'

	if validationRoutineFound and firstErrorDontSubmit == 0:
		print '	if (error_in_form) {'
		print '	  return false;'
		print '	}'
		print '	else {'
		print '	  return true;'
		print '	}'
		print '  }\n'

	form_routine['submitForm'] = {'number_arguments' : 1}
	print "function submitForm(form) {"
	if validationRoutineFound:
		print '  var valid_form = false;'
	print '  if (form.action.value == "delete" || form.action.value == "delete_item") {'
	print '	if (window.confirm("Are you sure you want to delete this item?")) {'
	print "	  return true;"
	print "	}"
	print "	else {"
	print "	  return false;"
	print "	}"
	print "  }"

	if validationRoutineFound:
		print '  valid_form = validate_form(form);'
		print '  if (valid_form) {'
		print '	return true;'
		print '  }'
		print '  else {'
		print '	return false;'
		print '  }'
	else:
		print "  return true;"

	print "}\n"	

	print '</SCRIPT>'

def javaScript(form_name, assign_hidden_authentication=0):
	"""
	Generates HTML for a variety of javascript functions to handle
	form processing.  HTML is written to standard output
	"""

	print "<SCRIPT>"
	print "<!-- For browser without JavaScript support"

	print 'function confirmDialog(message) {\n'
	print '	if (window.confirm(message)) {\n'
	print "	  return true;\n"
	print "	}\n"
	print "	else {\n"
	print "	  return false;\n"
	print "	}\n"
	print '}\n'

	print 'function goto_url(url) {\n'
	print '  window.location.href = url;\n'
	print '  return true;\n'
	print '}\n'

	print 'function toMenu (menuName) {\n'
	print '  window.history.go(menuName);\n'
	print '  return true;\n'
	print '}\n'

	print "function submitForm(form) {\n"
	print '  if (form.action.value == "delete" || form.action.value == "delete_item") {\n'
	print '	if (window.confirm("Are you sure you want to delete this item?")) {\n'
	print "	  return true;\n"
	print "	}\n"
	print "	else {\n"
	print "	  return false;\n"
	print "	}\n"
	print "  }\n"
	print "  return true;\n"
	print "}"	

	print "function execute(action_name, id_key) {\n"
	print "  var status = false;\n"
	print '  document.' + form_name + '.action.value = action_name;\n'
	print '  document.' + form_name + '.key_id.value = id_key;\n'
	print '  status = submitForm(' + 'document.' + form_name +');\n'
	print '  if (status == true) {\n'
 
	if assign_hidden_authentication == 1:
		print '	document.' + form_name + '.uHidden.value = document.' + form_name + '.username.value;\n'
		print '	document.' + form_name + '.pHidden.value = document.' + form_name + '.password.value;\n'

	print '	document.' + form_name + '.submit();\n'
	print '	return true;\n'
	print '  }\n'
	print '  else {\n'
	print "	return false;\n"
	print '  }\n'
	print "}\n"

	print "function process_item(action_name, item_no) {\n"
	print "  var status = false;\n"
	print '  document.' + form_name + '.action.value = action_name;\n'
	print '  document.' + form_name + '.item_no.value = item_no;\n'
	print '  status = submitForm(' + 'document.' + form_name +');\n'
	print '  if (status == true) {\n'
 
	if assign_hidden_authentication == 1:
		print '	document.' + form_name + '.uHidden.value = document.' + form_name + '.username.value;\n'
		print '	document.' + form_name + '.pHidden.value = document.' + form_name + '.password.value;\n'

	print '	document.' + form_name + '.submit();\n'
	print '	return true;\n'
	print '  }\n'
	print '  else {\n'
	print "	return false;\n"
	print '  }\n'
	print "}\n"

	print "function displayHint(hint) {\n"
	print "  window.status = hint;\n"
	print "  return true;\n"
	print "}\n"

	print "function carriage_return () {\n"
	print "  if (navigator.appVersion.lastIndexOf ('Win') != -1) {\n"
	print '	return "\\r\\n";\n'
	print "  }\n"
	print "  return \"\\n\";\n"
	print "}\n"
	
	print "function checkBlankField(theField, fieldName) {\n"
	print "  var str = theField.value;\n"
	print "  var blankStr = true;\n"
	print "  for (var i = 0; i < str.length; i++) {\n"
	print "	var ch = str.substring(i,i+1);\n"
	print '	if (ch != " ") {\n'
	print "	  blankStr = false;\n"
	print "	  break;\n"
	print "	}\n"
	print "  }\n"
	
	print "  if (blankStr || str.length == 0) {\n"
	print '	document.' + form_name + '.alerts.value = fieldName + " can not be blank!" + carrage_return() + document.' + form_name + '.alerts.value;\n'
	print "	return true;\n"
	print "  }\n"
	print "  else {\n"
	print "	return false;\n"
	print "  }\n"
	print "}\n"

	print "function goto_url(url) {"
	print "  window.location.href = url;"
	print "  return true;"
	print "}\n"
	

	print "// -->"
	print "</SCRIPT>"

def tableColumn(data, align='center'):
	"""
	Generates HTML table column tags with data inserted in the column
	optional alignment specifier for column is provided.  HTML is written
	to standard output.
	"""

	print '<TD ALIGN=' + align + ' NOWRAP><FONT FACE="Arial,Helvetica" SIZE="-1">' + data + '</FONT></TD>'

def header(headers):
	pass

def tableDataToDb(table_data,table_name):
	"""
	Converts table data items specified by table_name to data values that
	can be stored in the database.  Resultant db data created is returned.
	"""

	dbData = {}

	for field_name in table_data[table_name].keys():

		if table_data[table_name][field_name]["type"] == 'BOOL':

			if string.lower(table_data[table_name][field_name]["value"]) == "yes":
				dbData[field_name] = 't'
			elif string.lower(table_data[table_name][field_name]['value']) == 'no':
				dbData[field_name] = 'f'

		elif table_data[table_name][field_name]["type"] == 'INT4':
			dbData[field_name] = int(table_data[table_name][field_name]["value"])

		elif table_data[table_name][field_name]["type"] == 'FLOAT4':
			dbData[field_name] = float(table_data[table_name][field_name]["value"])

		else:
			dbData[field_name] = string.strip(table_data[table_name][field_name]["value"])

	return dbData

def dbToTableData(table_data, table_name, db):
	"""
	Converts data found in the database fields specified by the dictionary db
	to data that can be stored in table_data designated by table_name.
	Specifically handles BOOL conversion to Yes, No values and converted
	numerically stored db data into strings since all table data values are
	stored as strings.  The values are stripped of whitespace on the left and
	right.  The resultant table_data is returned.
	"""

	for field_name in db.keys():

		if table_data[table_name].has_key(field_name):

			if table_data[table_name][field_name]["type"] == 'BOOL':

				if db[field_name] == 't':
					table_data[table_name][field_name]["value"] = "Yes"
				else:
					table_data[table_name][field_name]["value"] = "No"

			elif table_data[table_name][field_name]["type"] == 'INT4' or \
				 table_data[table_name][field_name]["type"] == 'FLOAT4':
				table_data[table_name][field_name]["value"] = `db[field_name]`

			else:
				table_data[table_name][field_name]["value"] = db[field_name]

			string.strip(table_data[table_name][field_name]["value"])

	return table_data

def cookieToTableData(table_data,table_name,cookie,key=None):
	"""
	Converts the data fields in cookie to table_data specified by table_name
	the id of the table can optionally be set.  Cookie field names must match
	table_data field names in table_name for this to work as is the case with
	all of the mapping functions in this file.  The resultant table_data
	will be returned
	"""
	for field_name in cookie.keys():
		if table_data[table_name].has_key(field_name):
			table_data[table_name][field_name]['value'] = cookie[field_name].value

	if key != None:
		table_data[table_name]['id'] = key

	return table_data

def retainAllHiddenFormFields(table_data,form):
	
	for field_name in form.keys():

		if field_name[-6:] == 'hidden':

			start = string.index(field_name,'_')+1
			end = string.rindex(field_name,'_',start)

			table_name = field_name[:string.index(field_name,'_')]

			textbox(None,field_name,form[field_name].value,table_data[table_name][field_name[start:end]]['form_size'],table_data[table_name][field_name[start:end]]['form_size'],None,None,'hidden')
			
def formToHiddenFields(table_data,table_name,form):

	for field_name in form.keys():
		if table_data[table_name].has_key(field_name):
			textbox(None,table_name + '_' + field_name + '_hidden',form[field_name].value,table_data[table_name][field_name]['form_size'],table_data[table_name][field_name]['form_size'],None,None,'hidden')

def tableDataToCookie(table_data,table_name,cookie,key=None):

	for field_name in table_data[table_name].keys():
		cookie[field_name] = table_data[table_name][field_name]["value"]

	if key != None:
		cookie['id'] = table_data[table_name]["id"]["value"]

	return cookie

def formToTableData(table_data,table_name, form, key=None):

	for field_name in form.keys():
		if table_data[table_name].has_key(field_name):			
			table_data[table_name][field_name]["value"] = form[field_name].value

	if key != None:
		table_data[table_name]["id"]["value"] = key

	return table_data

def hiddenFieldsWithTableNameToTableData(table_data,table_name,form,key=None):
	"""
	Examines the form fields in argument form that are hidden fields or 
	specifically are named {table_name}{field_in_table_name}_hidden.  Then 
	sets the table_data, table_name_field_name entry for this field to the 
	value of the hidden field. Returns resultant table_data items
	"""

	for field_name in form.keys():

		# if the table name is the first part of the field name and field is a hidden field
		if field_name[:len(table_name)] == table_name and field_name[-6:] == 'hidden':
			start = string.index(field_name,'_')+1
			end = string.rindex(field_name,'_',start)

			if table_data[table_name].has_key(field_name[start:end]):			
				table_data[table_name][field_name[start:end]]["value"] = form[field_name].value 

	if key != None:
		table_data[table_name]["id"]["value"] = key

	return table_data
	
def formToDict(form):
	""" 
	Converts a module cgi dictionary of form field values to a 
	simple dictionary[field_name] = value dictionary
	Returns the dictionary.  Basically loads form[field_name].value
	into a dictionary[field_name] = value representation
	"""

	dict = {}
	keyitems = form.keys()

	for i in keyitems:
		dict[i] = form[i].value

	return dict

def formOptionListToList(form, optionListName):
	optionList = []
	optionListData = form[optionListName]
	if type(optionListData) is type([]):
		for option in optionListData:
			optionList.append(option.value)
	else:
		optionList.append(optionListData.value)

	return optionList

def getFormData(keep_blank_values=1):
	"""
	Returns the fields and values of a form that has been submitted to
	a CGI script.  By default form fields that the operator has not entered
	data into or are blank are submitted to the CGI.  The CGI module would
	not give the CGI these fields by default, they would merely not exist.
	"""
	return cgi.FieldStorage(keep_blank_values=1)

def htmlContentType(cookies=None):		
	"""
	Generates the content type header that web browser look for in order
	to determine how it should process the data to follow.  Will optionally
	generate the cookie header text which sets the values of cookies
	"""

	print "Content-type: text/html"
	if cookies != None:
		print cookies
	print						   

def title(title_data, store_name='FSBO WV'):
	"""
	Generates HTML to standard output for the title of the web page
	"""
	print '<TITLE>' + store_name + ': ' + title_data + '</TITLE>'

def executeSQL(db, sqlStatement):
	"""
	Execute a sql statement specified by sqlStatement for the already
	open db connection designate by db
	Returns a queryResult type, see above
	"""

	try:

		pgqueryObject = db.query(sqlStatement)

	except TypeError:
		return {'status' : 'error', 'message' : "TypeError: Bad Argument type, or too many arguments", result : None} 
	except ValueError:
		return {'status' : 'error', 'message' : "ValueError: Empty SQL Query", result : None} 
	except _pg.error, message:
		return {'status' : 'error', 'message' : message, 'result' : None} 

	# sql statement is not a select or insert
	if pgqueryObject == None:
		return {'status' : 'success', 'message' : "SQL Statement processed returning nothing", 'result' : None}

	# sql statement is an insert or update statement
	if type(pgqueryObject) is types.IntType:
		return {'status' : 'success', 'message' : "SQL Statement processed return number rows affected", 'result' : pgqueryObject}

	# sql statement is a select
	result = pgqueryObject.dictresult()

	return {'status' : 'success', 'message' : "SQL Query processed returning rows fetched", 'result' : result}

def create_tables(db, table_data, echoStatement=0):

	table_name_keys = table_data.keys()
	
	table_name_keys.sort()

	# loop through each table name
	for table_name in table_name_keys:

		sqlStatement = "DROP TABLE " + table_name

		queryResult = executeSQL(db, sqlStatement)

		sqlStatement = "CREATE TABLE "

		sqlStatement = sqlStatement + table_name + " ("

		column_name_keys = table_data[table_name].keys()

		column_name_keys.sort()

		creation_order = []

		for i in xrange(0,len(column_name_keys)):
			creation_order.append("")

		for i in column_name_keys:
			creation_order[int(table_data[table_name][i]['display_order'])-1] = i

		# put id key up front
		for column_name in creation_order:

			sqlStatement = sqlStatement + buildColumnDeclaration(table_name, column_name, table_data)
			
			sqlStatement = sqlStatement + ", "

		sqlStatement = sqlStatement[:-2] + ")"

		if echoStatement == 1:
			print "\nSQL Statement:\n" + sqlStatement + "\nPerformed successfully"

		queryResult = executeSQL(db, sqlStatement)

		if queryResult['status'] != 'success':
			return queryResult

	return {'status' : 'success', 'message' : "Database tables created successfully", 'result' : None}

def connectDB(username, password, database):

	try:

		db = DB(database, 'localhost', 5432, None, None, username, password)

	except TypeError:
		return {'status' : 'error', 'message' : "Bad Argument type, or too many arguments", 'result' : None}

	except SyntaxError:
		return {'status' : 'error', 'message' : "Duplicate argument definition in connect", 'result' : None}

	except _pg.error, message:
		return {'status' : 'error', 'message' : message, 'result' : None}

	return {'status' : 'success', 'message' : 'Database connection succeeded', 'result' : db}

def executeSqlItemList(db, sqlList, echoStatement=0,ignoreErrors=0):

	for sqlItem in sqlList:

		queryResult = executeSQL(db, sqlItem)
		
		if not ignoreErrors:
			if queryResult["status"] != 'success':
				return queryResult

		if echoStatement == 1:
			print "\nSQL Statement: " + sqlItem + '\nPerformed with status: ' + queryResult['status']
			if queryResult['status'] != 'success':
				print 'Details: ' + queryResult['message']

	return {'status' : "success", 'message' : "Items in SqlItemList processed", 'result' : None}

def table_data_to_email(table_data, table_name, displayOrder='useValues'):

	email_form = ''

	field_name_keys = table_data[table_name].keys()

	if displayOrder == 'sort':
		field_name_keys.sort()

	elif displayOrder == 'useValues':
		display_list = []

		# build display list array
		for i in xrange(0,len(field_name_keys)):
			display_list.append("")

		# load display_list entries with table display order field_names
		for i in field_name_keys:
			display_list[int(table_data[table_name][i]['display_order'])-1] = i

		field_name_keys = display_list

	for field_name in field_name_keys:

		if table_data[table_name][field_name]["display"] == 'editable' or \
		   table_data[table_name][field_name]["display"] == 'read-only':

			email_form = email_form + table_data[table_name][field_name]['label'] + ': '

			# field specified in table data as editable
			if table_data[table_name][field_name]['display'] == 'editable' or \
			   table_data[table_name][field_name]["display"] == 'read-only':

				email_form = email_form + table_data[table_name][field_name]['value'] + '\n'

	return email_form

def display_form(table_data, table_name, editable=1, displayOrder='useValues', displayHeader=1, db=None):

	print "<TABLE BORDER=1>"

	if editable == 1:
		print '<CAPTION>Field Labels in <B><FONT COLOR=RED>Red</FONT></B> or <B>Bold</B> on Mononchrome Displays are Required</CAPTION>'

	if displayHeader:
		print '<TR><TH>Field Name</TH><TH>Value</TH>'
		
	if editable == 1:
		print '<TH>Format</TH>'

	print '</TR>'

	field_name_keys = table_data[table_name].keys()

	if displayOrder == 'sort':
		field_name_keys.sort()

	elif displayOrder == 'useValues':
		display_list = []

		# build display list array
		for i in xrange(0,len(field_name_keys)):
			display_list.append("")

		# load display_list entries with table display order field_names
		for i in field_name_keys:
			display_list[int(table_data[table_name][i]['display_order'])-1] = i

		field_name_keys = display_list

	for field_name in field_name_keys:

		if table_data[table_name][field_name]["display"] == 'editable' or \
		   table_data[table_name][field_name]["display"] == 'read-only':

			print '<TR>'

			if editable == 1:

				if table_data[table_name][field_name].has_key('required'):

					if  table_data[table_name][field_name]['required']:
						print '<TD ALIGN=LEFT' + ' NOWRAP><FONT FACE="Arial,Helvetica" COLOR=RED SIZE="-1">' + '<B>' + table_data[table_name][field_name]["label"] + ':' + '</B>' + '</FONT></TD>'
					else:
						print '<TD ALIGN=LEFT' + ' NOWRAP><FONT FACE="Arial,Helvetica" COLOR=BLACK SIZE="-1">' + table_data[table_name][field_name]["label"] + ':' + '</FONT></TD>'
				else:
					print '<TD ALIGN=LEFT' + ' NOWRAP><FONT FACE="Arial,Helvetica" COLOR=BLACK SIZE="-1">' + table_data[table_name][field_name]["label"] + ':' + '</FONT></TD>'

			else:
					print '<TD ALIGN=LEFT' + ' NOWRAP><FONT FACE="Arial,Helvetica" COLOR=BLACK SIZE="-1">' + '<B>' + table_data[table_name][field_name]["label"] + ':</B>' + '</FONT></TD>'

			print '<TD ALIGN=LEFT NOWRAP>'

			# field specified in table data as editable
			if table_data[table_name][field_name]["display"] == 'editable':

				# caller wants for displayed editable
				if editable == 1:

					if table_data[table_name][field_name]["type"] == 'BOOL':
						if table_data[table_name][field_name]["value"] == 'Yes':
							optionMenu(field_name,"1",["Yes","No"],["SELECTED",""])
						else:
							optionMenu(field_name,"1",["Yes","No"],["","SELECTED"])

					else:
						if int(table_data[table_name][field_name]["form_size"]) > 64:
							textarea(table_name,
									 field_name,
									 table_data[table_name][field_name]["value"],
									 `int(table_data[table_name][field_name]["form_size"]) / 64`,
									 '64',
									 table_data[table_name][field_name]["leaveFocus"],
									 table_data[table_name][field_name]["gainFocus"])

						else:
							if table_data[table_name][field_name].has_key('lov'):
								# display an option menu since the field is only allowed to
								# be set to the item in a list of value table

								dbResult = executeSQL(db, table_data[table_name][field_name]['lov'])
								
								if dbResult['status'] != 'success':
									# error could not process sql lov
									pass
								else:
									
									result = dbResult['result']
									option_items = []
									selection_list = []

									for i in xrange(0,len(result)):
										item_list = result[i].values()
										option_items.append(item_list[0])
										if item_list[0] == table_data[table_name][field_name]['value']:
											selection_list.append("SELECTED")
										else:
											selection_list.append("")

									optionMenu(field_name,"1",option_items,selection_list)

							else:
								if table_data[table_name][field_name].has_key('form_input_type'):
									form_input_type = table_data[table_name][field_name]['form_input_type']
								else:
									form_input_type = 'text'

								textbox(table_name,
										field_name,
										table_data[table_name][field_name]["value"],
										table_data[table_name][field_name]["form_size"],
										table_data[table_name][field_name]["form_size"],
										table_data[table_name][field_name]["leaveFocus"],
										table_data[table_name][field_name]["gainFocus"],
										form_input_type)
				else:
				
					print table_data[table_name][field_name]["value"]

			else:
				print table_data[table_name][field_name]["value"]
				
			print '</TD>'

			if table_data[table_name][field_name].has_key("format"):
				if editable == 1:
					tableColumn(table_data[table_name][field_name]["format"],'left')

			print '</TR>'

	print '</TABLE>'

def init_table_data(table_data, table_name):

	field_name_keys = table_data[table_name].keys()
	
	for field_name in field_name_keys:
		if table_data[table_name][field_name]["default"] != None:
			table_data[table_name][field_name]["value"] = table_data[table_name][field_name]["default"]
		else:
			table_data[table_name][field_name]["value"] = ''

	return table_data

def executeQuery(db, table_data, table_name, queryFields, whereFields, itemFunctions, queryItemFunctionsHtml, orderClause='ORDER BY id', queryItemKey='id', whereClause=None,ignoreFields=None,queryButtonAction="return execute('query')"):
	"""
	Executes a user specified query from the column headers on an existing
	or 
	"""

	# allocate the options list
	options = []
	selectedOptions = []

	# table names
	#fieldNames = table_data[table_name].keys()
	fieldNames = []

	# set options to the label associated with the field names of the keys in table name
	for columnName in table_data[table_name].keys():
		# load options list with column labels for each column that exists in table except any that have been specified to be ignored
		if ignoreFields != None:
			if columnName not in ignoreFields:
				options.append(table_data[table_name][columnName]["label"])
				selectedOptions.append("")
				fieldNames.append(columnName)
		else:
			options.append(table_data[table_name][columnName]["label"])
			selectedOptions.append("")
			fieldNames.append(columnName)

	options.append("None")	
	selectedOptions.append("")

	print '<FONT FACE="Arial,Helvetica" SIZE="-2">'
	print '<TABLE BORDER=1>'
	print '<TR>'

	# for each field in query fields list
	for columnNumber in xrange(0,len(queryFields)):

		print '<TH>'

		# the item that is supposed to be the field name is found by
		# using the index of the field name 
		selectedOptions[fieldNames.index(queryFields[columnNumber])] = "SELECTED"

		# generate the options menu with the current field to display for this column
		optionMenu('columnOption' + `columnNumber`, '1', options, selectedOptions)

		selectedOptions[fieldNames.index(queryFields[columnNumber])] = ""

		relops, selRelops = queryRelops(table_data, table_name, queryFields[columnNumber])

		# generate the options menu with the current field to display for this column
		optionMenu('columnRelop' + `columnNumber`, '1', relops, selRelops)

		textbox(table_name, 'columnMatch' + `columnNumber`, '', '10', table_data[table_name][queryFields[columnNumber]]["form_size"],None,None)

		print '</TH>'
		
	print '<TH><FONT FACE="Arial,Helvetica" SIZE="-1">Add Column<BR>'

	# generate the options menu with the current field to display for this column
	# remove the None from options list
	
	selectedOptions[len(selectedOptions)-1] = "SELECTED"
	optionMenu('addColumn', '1', options, selectedOptions)

	if queryButtonAction != None:
		print '<INPUT NAME="subQuery" type="button" value=" Query " onClick="%s">' % (queryButtonAction)

	print '</TH>'
	print '</TR>'

	sqlStatement = 'SELECT '

	sqlStatement = sqlStatement + queryItemKey + ', '

	for columnNumber in xrange(0,len(queryFields)):
		sqlStatement = sqlStatement + queryFields[columnNumber] + ', '
		
	sqlStatement = sqlStatement[:-2]

	sqlStatement = sqlStatement + ' FROM ' + table_name

	if whereFields != None and whereFields != []:
		sqlStatement = sqlStatement + " WHERE "

		for whereFieldNumber in xrange(0,len(whereFields)):
			sqlStatement = sqlStatement + whereFields[whereFieldNumber] + ' AND '

		sqlStatement = sqlStatement[:-5]

	if whereClause != None:
		if whereFields != None and whereFields != []:
			sqlStatement = sqlStatement + ' AND ' + whereClause
		else:
			sqlStatement = sqlStatement + ' WHERE ' + whereClause
			
	sqlStatement = sqlStatement + ' ' + orderClause

	queryResult = executeSQL(db, sqlStatement)
	
	if queryResult['status'] != 'success':

		return (queryResult, sqlStatement)

	else:

		result = queryResult['result']

		# loop through all rows returned from query
		for row in xrange(0,len(result)):

			table_data = dbToTableData(table_data, table_name, result[row])

			print '<TR>'

			# for each column specified by queryFields
			for col in xrange(0,len(queryFields)):

				# generate a table column
				tableColumn(table_data[table_name][queryFields[col]]["value"])

			if itemFunctions == 'query':
				print queryItemFunctionsHtml(table_data[table_name][queryItemKey]["value"])

			print '</TR>'

		print '</TABLE>'

	return (queryResult, sqlStatement)

def getQueryWhereFields(form, table_data, table_name):
	
	if form.has_key("columnOption0"):

		queryFields = []
		whereFields = []

		found = 0
		numCol = 0

		while 1:
			if form.has_key("columnOption" + `numCol`):
				numCol = numCol + 1
			else:
				break
						
		# loop through all columns on query page
		for columnNumber in xrange(0,numCol):
			
			for columnName in table_data[table_name].keys():
				
				if table_data[table_name][columnName]["label"] == form["columnOption" + `columnNumber`].value:
					if string.strip(form["columnMatch" + `columnNumber`].value) != "":
						if (table_data[table_name][columnName]["type"] == 'VARCHAR') or \
						   (table_data[table_name][columnName]["type"] == 'DATE') or \
						   (table_data[table_name][columnName]["type"] == 'BOOL'):

							whereFields.append(columnName + " " + form["columnRelop" + `columnNumber`].value + " '" + form["columnMatch" + `columnNumber`].value + "'")

						else:

							if table_data[table_name][columnName]['type'] == 'DECIMAL':
								# have to cast db items declared as decimal
								whereFieldItem = 'float8(' + columnName + ") " + form["columnRelop" + `columnNumber`].value + " " + form["columnMatch" + `columnNumber`].value
							else:
								whereFieldItem = columnName + " " + form["columnRelop" + `columnNumber`].value + " " + form["columnMatch" + `columnNumber`].value

							whereFields.append(whereFieldItem)
							
					queryFields.append(columnName)
					break

		if form.has_key("addColumn"):
			if form["addColumn"].value != "None":

				for columnName in table_data[table_name].keys():				
					if table_data[table_name][columnName]["label"] == form["addColumn"].value:
						queryFields.append(columnName)

		return (queryFields, whereFields)

	else:
		return (None, None)

def queryRelops(table_data, table_name, queryField):

	if table_data[table_name][queryField]["type"] == 'VARCHAR':
		relOptions = []
		relOptions.append("<")
		relOptions.append("<=")
		relOptions.append("=")
		relOptions.append("!=")
		relOptions.append(">")
		relOptions.append(">=")
		relOptions.append("like")
		selRelops = []
		selRelops.append("")
		selRelops.append("")
		selRelops.append("SELECTED")
		selRelops.append("")
		selRelops.append("")
		selRelops.append("")
		selRelops.append("")
		
	elif table_data[table_name][queryField]["type"] == 'BOOL':
		relOptions = []
		relOptions.append("=")
		relOptions.append("!=")
		selRelops = []
		selRelops.append("SELECTED")
		selRelops.append("")
					
	elif table_data[table_name][queryField]["type"] == 'INT4' or \
		 table_data[table_name][queryField]["type"] == 'FLOAT4' or \
		 table_data[table_name][queryField]["type"] == 'DECIMAL' or \
		 table_data[table_name][queryField]["type"] == 'DATE':
		relOptions = []
		relOptions.append("<")
		relOptions.append("<=")
		relOptions.append("=")
		relOptions.append("!=")
		relOptions.append(">")
		relOptions.append(">=")
		selRelops = []
		selRelops.append("")
		selRelops.append("")
		selRelops.append("SELECTED")
		selRelops.append("")
		selRelops.append("")
		selRelops.append("")
		
	return (relOptions, selRelops)

def alertsArea(form, value):
	print "<BR>Alerts:"
	textarea(None, 'alerts', value, '2', '64', None, None)

	if form.has_key("alerts"):
		textbox(None, 'hidden_alerts', form["alerts"].value, '320', '320', None, None, 'hidden')
	else:
		textbox(None, 'hidden_alerts', '', '320', '320', None, None, 'hidden')

def storeHiddenFields(username, password):
	textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
	textbox(None, 'action', '', '10', '10', None, None, 'hidden')
	textbox(None, 'uHidden', username, '9', '9', None, None, 'hidden')
	textbox(None, 'pHidden', password, '8', '8', None, None, 'hidden')
	textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')

def createHiddenFields(username, password):
	textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
	textbox(None, 'action', '', '10', '10', None, None, 'hidden')
	textbox(None, 'uHidden', username, '9', '9', None, None, 'hidden')
	textbox(None, 'pHidden', password, '8', '8', None, None, 'hidden')
	textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')

def viewPropertiesHiddenFields(username, password):
	textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
	textbox(None, 'action', '', '10', '10', None, None, 'hidden')
	textbox(None, 'uHidden', username, '9', '9', None, None, 'hidden')
	textbox(None, 'pHidden', password, '8', '8', None, None, 'hidden')
	textbox(None, 'username', username, '9', '9', None, None, 'hidden')
	textbox(None, 'password', password, '8', '8', None, None, 'hidden')
	textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')

def storeHiddenFields(username, password):
	textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
	textbox(None, 'action', '', '10', '10', None, None, 'hidden')
	textbox(None, 'uHidden', username, '9', '9', None, None, 'hidden')
	textbox(None, 'pHidden', password, '8', '8', None, None, 'hidden')
	textbox(None, 'username', username, '9', '9', None, None, 'hidden')
	textbox(None, 'password', password, '8', '8', None, None, 'hidden')
	textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')

def queryHiddenFields(username, password):
	textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
	textbox(None, 'action', '', '10', '10', None, None, 'hidden')
	textbox(None, 'uHidden', username, '9', '9', None, None, 'hidden')
	textbox(None, 'pHidden', password, '8', '8', None, None, 'hidden')
	textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')

def editHiddenFields(username, password, key_id=''):
	textbox(None, 'key_id', key_id, '10', '10', None, None, 'hidden')
	textbox(None, 'action', '', '10', '10', None, None, 'hidden')
	textbox(None, 'uHidden', username, '9', '9', None, None, 'hidden')
	textbox(None, 'pHidden', password, '8', '8', None, None, 'hidden')
	textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')

def queryItemFunctionsHtmlNoEdit(db_key):
	return '<TD ALIGN=CENTER NOWRAP><INPUT NAME="delete" type="button" value=" Delete " onClick="return execute(' + "'delete'" + ", '" + db_key + "'" + ')"><INPUT NAME="view" type="button" value=" View " onClick="return execute(' + "'view'" + ", '" + db_key + "'" + ')">'

def queryItemFunctionsHtml(db_key):
	return '<TD ALIGN=CENTER NOWRAP><INPUT NAME="edit" type="button" value=" Edit " onClick="return execute(' + "'edit'" + ", '" + db_key + "'" + ')"><INPUT NAME="delete" type="button" value=" Delete " onClick="return execute(' + "'delete'" + ", '" + db_key + "'" + ')"><INPUT NAME="view" type="button" value=" View " onClick="return execute(' + "'view'" + ", '" + db_key + "'" + ')">'

def viewPropertiesFunctionsHtml(db_key):
	return '<TD ALIGN=CENTER NOWRAP><FONT FACE="Arial,Helvetica" SIZE=-1"><INPUT NAME="view" type="button" value=" View " onClick="return execute(' + "'view'" + ", '" + db_key + "'" + ')"></FONT></TD>'

def storeFunctions():
	print '<TABLE><TR><TD ALIGN=CENTER NOWRAP><INPUT NAME="viewcart" type="button" value=" View Cart " onClick="return execute(' + "'viewcart'" + ')"></TD><TD ALIGN=CENTER NOWRAP><INPUT NAME="checkout" type="button" value=" Check Out " onClick="return execute(' + "'checkout'" + ')"></TD></TABLE>'

def queryItemFunctions(db_key):
	tableColumn('<INPUT NAME="edit" type="button" value=" Edit " onClick="return execute(' + "'edit'" + ", '" + db_key + "'" + ')"><INPUT NAME="delete" type="button" value=" Delete " onClick="return execute(' + "'delete'" + ", '" + db_key + "'" + ')"><INPUT NAME="view" type="button" value=" View " onClick="return execute(' + "'view'" + ", '" + db_key + "'" + ')">')

def viewPropertiesFunctionButtons(help_pdf='http://www.linuxden.com/XdenCommerce/sum.pdf'):
	print '<HR>'
	print '<TABLE>'
	print '<TR>'
	tableColumn('<INPUT NAME="query" type="button" value=" Query " onClick="return execute(' + "'query'" + ')">')
	tableColumn('<INPUT TYPE="button" NAME="help" VALUE=" Help " onClick="return goto_url (' + "'" + help_pdf + "'" + ')">')
	print '</TR>'
	print '</TABLE>'

def queryFunctionButtons(loginOk=1, help_pdf='http://www.linuxden.com/XdenCommerce/sum.pdf'):
	print '<HR>'
	print '<TABLE>'
	print '<TR>'
	tableColumn('<INPUT NAME="query" type="button" value=" Query " onClick="return execute(' + "'query'" + ')">')
	if loginOk == 1:
		  tableColumn('<INPUT NAME="create" type="button" value=" Create " onClick="return execute(' + "'create'" + ')">')	
	tableColumn('<INPUT TYPE="button" NAME="help" VALUE=" Help " onClick="return goto_url (' + "'" + help_pdf + "'" + ')">')
	print '</TR>'
	print '</TABLE>'

def createFunctionButtons(db_key, menu_name, help_pdf):
	print '<HR>'
	print '<TABLE>'
	print '<TR>'
	tableColumn('<INPUT NAME="create" type="button" value=" Create " onClick="return execute(' + "'save','" + db_key + "'" + ')">')
	tableColumn('<INPUT TYPE="button" NAME="return_to_menu" VALUE=" Listing " onClick="return goto_url (' + "'" + menu_name + "'" + ')">')
	tableColumn('<INPUT TYPE="button" NAME="help" VALUE=" Help " onClick="return goto_url (' + "'" + help_pdf + "'" + ')">')
	print '</TR>'
	print '</TABLE>'

def editFunctionButtons(db_key, menu_name, help_pdf):
	print '<HR>'
	print '<TABLE>'
	print '<TR>'
	tableColumn('<INPUT NAME="save" type="button" value=" Save " onClick="return execute(' + "'save'" + ",'" + db_key + "'" + ')">')
	tableColumn('<INPUT NAME="delete" type="button" value=" Delete " onClick="return execute(' + "'delete'" + ",'" + db_key + "'" + ')">')	
	tableColumn('<INPUT NAME="view" type="button" value=" View " onClick="return execute(' + "'view'" + ", '" + db_key + "'" + ')">')
	tableColumn('<INPUT TYPE="button" NAME="return_to_menu" VALUE=" Listing " onClick="return goto_url (' + "'" + menu_name + "'" + ')">')
	tableColumn('<INPUT TYPE="button" NAME="help" VALUE=" Help " onClick="return goto_url (' + "'" + help_pdf + "'" + ')">')
	print '</TR>'
	print '</TABLE>'

def viewFunctionButtons(menu_name, help_pdf):
	print '<HR>'
	print '<TABLE>'
	print '<TR>'
	tableColumn('<INPUT TYPE="button" NAME="return_to_menu" VALUE=" Listing " onClick="return goto_url (' + "'" + menu_name + "'" + ')">')
	tableColumn('<INPUT TYPE="button" NAME="help" VALUE=" Help " onClick="return goto_url (' + "'" + help_pdf + "'" + ')">')
	print '</TR>'
	print '</TABLE>'

def selectAllColumnsSqlStatement(table_data,table_name,id,id_field_name='id'):

	sqlStatement = "SELECT "
	
	for columnName in table_data[table_name].keys():
		sqlStatement = sqlStatement + columnName + ", "
		
	sqlStatement = sqlStatement[:-2]
		
	sqlStatement = sqlStatement + " FROM " + table_name + " WHERE " + id_field_name + " = '" + id + "'"

	return sqlStatement
