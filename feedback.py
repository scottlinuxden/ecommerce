# $Id: feedback.py,v 1.6 2000/04/07 02:24:35 davis Exp davis $
# Copyright (C) 1999 LinuXden, All Rights Reserved
# Copright Statement at http://www.linuxden.com/copyrighted_apps.html
# 
import sys,os,cgi,glob,string
import declarations
import ecommerce
import os_utils
import commands

print "content-type: text/html\n"

from_email = 'support@clicktree.com'

def feedback_results(html_message, email_message, form):
	print "<HTML><HEAD><TITLE>Customer Feedback (Thank You)</TITLE></HEAD><BODY>"
	print '<h4>Customer Feedback (Thank You)</h4>'

	print html_message

	print "</BODY></HTML>"

	mail_support(email_message)
			
def mail_support(msg=""):
	
	if email:
                             
		content = "---------------------------------------\n"
		content = content + msg + '\n\n'
        
		for x in [ 'REQUEST_URI','HTTP_USER_AGENT','REMOTE_ADDR','HTTP_FROM','REMOTE_HOST','REMOTE_PORT','SERVER_SOFTWARE','HTTP_REFERER','REMOTE_IDENT','REMOTE_USER','QUERY_STRING','DATE_LOCAL' ]:
			if os.environ.has_key(x):
				line = "%s: %s\n" % (x, os.environ[x])
				content = content + line
		content = content + "---------------------------------------\n"

		try:
			ecommerce.send_email('www.linuxden.com',from_email,[email,'support@clicktree.com'],"Customer Feedback",content)
		except:
			print 'Sorry but your feedback could not be sent.'
			print 'Please contact <A HREF="mailto:support@clicktree.com">clickTree Support</A>'

def display_form(posturl):
	"Print the main form."
	print """<html>
<head>
<title>Customer Feedback</title>
<body>
<CENTER>
<B>Please provide us with the following information so that we<BR>may provide you with better products and services.</B>
<P>
<form action="/%s-cgi-bin/feedback.pyc" method="POST">
<TABLE BORDER=0>
<CAPTION><B>Customer Feedback Form</B></CAPTION>
<TR><TD><B>Your Name</B>:</TD><TD><input name="name" type="text" size="50" maxlength="50"></TD></TR>
<TR><TD><B>Street Address</B>:</TD><TD><input name="street" type="text" size="50" maxlength="50"></TD></TR>
<TR><TD><B>City</B>:</TD><TD><input name="city" type="text" size="50" maxlength="50"></TD></TR>
<TR><TD><B>State</B>:</TD><TD><input name="state" type="text" size="2" maxlength="2"></TD></TR>
<TR><TD><B>Zip</B>:</TD><TD><input name="zip" type="text" size="5" maxlength="5"></TD></TR>
<TR><TD><B>Phone Number</B>:</TD><TD><input name="phone" type="text" size="12" maxlength="12"></TD></TR>
<TR><TD><B>E-mail</B>:</TD><TD><input name="email" type="text" size="50" maxlength="50"></TD></TR>
</TABLE>
<CENTER>
<TABLE><tr>
<td><B>What are your interests?</b></td>
<td>
<b>Send me information about purchasing:</b>
</td>
</tr>
<tr>
<td><input type="checkbox" name="Buying"><b>Buying</b></td>
<td><input type="checkbox" name="Book"><b>Book "How to sell your home"</b></td>
</tr>
<tr>
<td><input type="checkbox" name="Selling"><b>Selling</b></td>
<td><input type="checkbox" name="Signs"><b>Directional
Signs &amp; Riders</b></td>
</tr>
<tr>
<td><input type="checkbox" name="Browsing"><b>Browsing</b></td>
<td><input type="checkbox" name="Subscription"><b>Subscription
to FSBO Magazine</b></td>
</tr>
<tr>
<td><input type="checkbox" name="Home"><b>A Specific Home &nbsp;</b><input type="text" name="code"></td>
<td><input type="checkbox" name="Advertising"><b>Advertising in FSBO Magazine</b></td>
</tr>
</TABLE>
<HR>
<input name="submit" type="submit" value="Send Comments">
</form>
</body>
</html>
""" % (declarations.store_info['db_name'])

if os.environ.has_key("HTTP_USER_AGENT"):
	browser = os.environ["HTTP_USER_AGENT"]
else:
	browser = "No Known Browser"

if os.environ.has_key("SCRIPT_NAME"):
	posturl = os.environ["SCRIPT_NAME"]
else:
	posturl = ""

form = cgi.FieldStorage(keep_blank_values=1)

if form.has_key('name'):

	table_data = declarations.define_tables()

	dbResult = ecommerce.connectDB(declarations.store_info['browser_username'], declarations.store_info['browser_password'], declarations.store_info['db_name'])
	
	if dbResult['status'] != 'success':

		print '<HTML><HEAD><TITLE>ERROR: Can not connect to db.</TITLE><BODY>'
		print 'Can not connect to database.'
		print '</BODY></HTML>'
		sys.exit(1)

	else:
	
		db = dbResult['result']
	    
		sqlStatement = ecommerce.selectAllColumnsSqlStatement(table_data,'store_info','1')

		dbResult = ecommerce.executeSQL(db, sqlStatement)

		if dbResult['status'] != 'success':
	
			email = 'support@clicktree.com'

		else:
	    
			result = dbResult['result']
	
			table_data = ecommerce.dbToTableData(table_data, 'store_info', result[0])

			email = table_data['store_info']['email']['value']
	
	html_msg = '<P>Your information has been submitted.'
	html_msg = html_msg + '<p>If you have requested information we will '
	html_msg = html_msg + 'respond to your request as soon as possible.'

	email_msg = ''
	email_msg = email_msg + 'Customer Feedback\n\n'
	email_msg = email_msg + 'Name: ' + form['name'].value + '\n'
	email_msg = email_msg + 'Street: ' + form['street'].value + '\n'
	email_msg = email_msg + 'City: ' + form['city'].value + '\n'
	email_msg = email_msg + 'State: ' + form['state'].value + '\n'
	email_msg = email_msg + 'Zip: ' + form['zip'].value + '\n'
	email_msg = email_msg + 'Phone: ' + form['phone'].value + '\n'
	email_msg = email_msg + 'E-mail: mailto:' + form['email'].value + '\n\n'

	email_msg = email_msg + 'Interests:\n'
	
	if form.has_key('Buying') and form['Buying'].value == 'on':
		email_msg = email_msg + '  Buying\n'
	if form.has_key('Selling') and form['Selling'].value == 'on':
		email_msg = email_msg + '  Selling\n'
	if form.has_key('Browsing') and form['Browsing'].value == 'on':
		email_msg = email_msg + '  Browsing\n'
	if form.has_key('Home') and form['Home'].value == 'on':
		email_msg = email_msg + '  Specific Home: ' + form['code'].value + '\n'

	email_msg = email_msg + '\nSend info:\n'

	if form.has_key('Book') and form['Book'].value == 'on':
		email_msg = email_msg + '  Book - How to sell your home\n'
	if form.has_key('Signs') and form['Signs'].value == 'on':
		email_msg = email_msg + '  Directional Signs & Riders\n'
	if form.has_key('Subscription') and form['Subscription'].value == 'on':
		email_msg = email_msg + '  Subscription to FSBO Magazine\n'
	if form.has_key('Advertising') and form['Advertising'].value == 'on':
		email_msg = email_msg + '  Advertising in FSBO Magazine\n'

	feedback_results(html_msg, email_msg, form)

	print "</BODY></HTML>"

else:

	display_form(posturl)
