# $Id: site_usage.py,v 1.1 2000/04/10 02:56:51 davis Exp $
# Copyright (C) 1999 LinuXden, All Rights Reserved
# Copright Statement at http://www.linuxden.com/copyrighted_apps.html
# 
import sys
import os
import cgi
import glob
import string
import declarations
import ecommerce
import os_utils
import authentication
import commands
import os_utils

upload_ceiling = 5000 * 1024 # 5 megabytes

email = 'support@clicktree.com'

dir_exclusions = ['./cgi-bin', './admin', './Counter']

def site_usage_results(html_message, email_message, form):
    print "<HTML><HEAD><TITLE>Site Usage</TITLE></HEAD><BODY>"
    print '<h3>Site Usage</h3>'
    print '<BLINK><STRONG>NOTE: All site maintenance is logged.</STRONG></BLINK><BR>'
    print html_message
    print "</BODY></HTML>"
    
    email_header = 'Website name: ' + form['website_name'].value + '\n'
    email_header = email_header + 'Username: ' + form['username'].value + '\n\n'
    mail_support(email_header + email_message)
    
def mail_support(msg=""):
		
    if email:
        
        content = "---------------------------------------\n"
        content = content + msg + '\n\n'
		
        for x in [ 'REQUEST_URI','HTTP_USER_AGENT','REMOTE_ADDR','HTTP_FROM','REMOTE_HOST','REMOTE_PORT','SERVER_SOFTWARE','HTTP_REFERER','REMOTE_IDENT','REMOTE_USER','QUERY_STRING','DATE_LOCAL' ]:
            if os.environ.has_key(x):
                line = "%s: %s\n" % (x, os.environ[x])
                content = content + line

        content = content + "---------------------------------------\n"
        
        ecommerce.send_email('www.linuxden.com','support@clicktree.com',[email],"Site Usage Report",content)

def display_form(display_files=0,alerts=None):
	print "<HTML>"

	print "<HEAD>"

	ecommerce.title("Site Maintenance (Usage)")

	print "</HEAD>"

	ecommerce.bodySetup()

	ecommerce.mainHeading('Site Maintenance')

	ecommerce.subHeading('Usage')

	ecommerce.formSetup("site_usage","site_usage",None,declarations.store_info['db_name'])

	if not display_files:
		print '<TABLE BORDER=0><TR><TD><B>Website Name</B>:</TD><TD><input name="website_name" type="text" size="50" maxlength="50"></TD></TR><TR><TD><B>Username</B>:</TD><TD><input name="username" type="text" size="9" maxlength="9"></TD></TR><TR><TD><B>Password:</B></TD><TD><input name="password" type="password" size="8" maxlength="8"></TD></TR></TABLE>'

	if display_files:
		if form.has_key('website_name'):
			website_value = form['website_name'].value
		else:
			website_value = form['website_name_hidden'].value
		
		os.chdir(os.path.join('/home',string.lower(string.strip(website_value))))

		file_list = os_utils.walk_list_files(
			directory_name='.',
			list_only_files=1,
			exclude_list = dir_exclusions,
			include_file_type=0,
			include_file_size=1)

		if len(file_list) > 25:
			list_size = 25
		else:
			list_size = len(file_list)

		status, du = os_utils.disk_usage(os.path.join('/home',website_value))

		if status == 'error':
			du_str = 'can not calculate file size'
		else:
			du_str = `du`
			
		print """
		<CENTER>
		<TABLE BORDER=0>
		<CAPTION><B>Site Usage:<B></CAPTION>
		<TR><TD WIDTH=300>
		All file sizes are in bytes.  The maximum amount of disk space allowed
		for your account is <B>%d</b> bytes.  The disk space allotment includes hit
		counter and administrative runtime files as well as any ecommerce
		engines you may have installed.  You are currently using <B>%s</b> bytes of
		your allowable disk space.""" % (upload_ceiling, du_str)

		if du > upload_ceiling:
			print '<p><B>You have exceeded the maximum disk space allotment for your website by <B>%d</b> bytes.' % (du - upload_ceiling)
			print '<p>Please remove files to lower your disk space usage or the monthly fee for your site will be increased.'
			print '<p>Contact <A HREF="mailto:sales@clicktree.com">clickTree Sales</A> for more information.</B>'

			mail_support('The site: ' + website_value + ' has exceeded their maximum disk space allotment of ' + `upload_ceiling` + ' bytes.\n' + 'The site is currently using ' + du_str + ' bytes of disk space\n' + 'The site has exceeded allotment allowed by ' + `du - upload_ceiling` + ' bytes.')

		else:
			print '<P>You have <B>%d</b> bytes of disk space left.' % (upload_ceiling - du)
			
		print '</TD></TR></TABLE>' 
		
		print '<BR><CENTER><B>File Sizes</B>:<BR><SELECT NAME="file_sizes" SIZE="%d" MULTIPLE>' % (list_size)

		for curfile in file_list:
			print '<OPTION>%s' % (curfile)
        
		print "</SELECT><BR>"

	if alerts != None:
		ecommerce.alertsArea(form,alerts)

	print '</CENTER>'
	
	print """
	<CENTER>
    <HR>
	"""
	
	if display_files:
		print '<input name="submit" type="submit" value="Refresh List">'
	else:
		print '<input name="submit" type="submit" value="Login">'
		

	print '</CENTER>'

	if display_files:
		if form.has_key('website_name'):
			print '<input name ="website_name_hidden" type="hidden" value="%s">' % (form['website_name'].value)
		else:
			print '<input name ="website_name_hidden" type="hidden" value="%s">' % (form['website_name_hidden'].value)
		
	print """
	<p align="right"><A HREF="mailto:support@clicktree.com">Contact Support Team</a>
    </form>
    </body>
    </html> 
	"""
    
if os.environ.has_key("HTTP_USER_AGENT"):
    browser = os.environ["HTTP_USER_AGENT"]
else:
    browser = "No Known Browser"

if os.environ.has_key("SCRIPT_NAME"):
    posturl = os.environ["SCRIPT_NAME"]
else:
    posturl = ""

ecommerce.htmlContentType()

form = ecommerce.getFormData()

if form.has_key('website_name'):

	status, valid = authentication.password_valid(
		passwd_filename='/home/' + string.lower(string.strip(form['website_name'].value)) + '/admin/upload_passwd',
        crypt_salt=string.lower(string.strip(form['website_name'].value)),
        username=form['username'].value,
	    password=form['password'].value)

	if status != 'success':
		html_msg = "Can not find password file for authentication of user.<BR>"
		email_msg = "Can not find password file for authentication of user."
		site_usage_results(html_msg, email_msg, form)
		sys.exit()
		
	if not valid:
		html_msg = "Invalid username or password specified.<BR>"
		email_msg = "Invalid username or password specified."
		site_usage_results(html_msg, email_msg, form)
		sys.exit()

	if not os.path.exists(os.path.join('/home', string.lower(string.strip(form['website_name'].value)))):
		html_msg = "Website, " + form['website_name'].value + ", does not exist.<BR>No site maintenance can be performed.<BR>"
		email_msg = "Website, " + form['website_name'].value + ", does not exist.\nNo site maintenance can be performed.\n"
		site_usage_results(html_msg, email_msg, form)
		sys.exit()
		
	display_form(display_files=1)
		
else:

	if form.has_key('website_name_hidden'):

		display_form(display_files=1)
			
	else:

		display_form()
