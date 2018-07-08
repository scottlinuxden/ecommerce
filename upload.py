# $Id: upload.py,v 1.11 2000/04/09 22:19:56 davis Exp davis $
# Copyright (C) 1999 LinuXden, All Rights Reserved
# Copright Statement at http://www.linuxden.com/copyrighted_apps.html
# 
import sys,os,cgi,glob,string
import declarations
import ecommerce
import os_utils
import authentication
import commands

upload_ceiling = 5000 * 1024 # 5 megabytes

link = "http://www.clicktree.com"

email = "support@clicktree.com"	 # where to email upload reports;

print "content-type: text/html\n"

def upload_results(html_message, email_message, form):
    print "<HTML><HEAD><TITLE>Upload Results</TITLE></HEAD><BODY>"
    print '<h3>Upload Results</h3>'
    print '<BLINK><STRONG>NOTE: All uploads are logged.</STRONG></BLINK><BR>'
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
        
        ecommerce.send_email('www.linuxden.com','support@clicktree.com',[email],"Upload Report",content)

def display_form(posturl):
    "Print the main form."
    print """<html>
<head>
<title>Site Maintenance</title>
<body>

<h3>Single File, Zip, or Tarfile upload:</h3>
<H3>Introduction</H3>
<P>This maintenance function will allow authorized users to upload a single file of type html, jpeg, or gif, or zip or tar
file archive to their website.  The tar file may be compressed with gzip.  The archive file size when extracted should not
exceed your maximum allowable disk space allotment for your site which is %d bytes.  If this happens all files that exceed the allotment will not be stored in your website.  It is therefore suggested that you maintain a complete copy of your site locally and change your local copy to how you would like it on Clicktree.com, create the archive of your local copy and upload the archive to Clicktree.com.  The archive filename should end with .zip .tgz</P>
<P>You may upgrade your disk space allotment via an e-mail request to the Clicktree.com <A HREF="mailto:support@clicktree.com">support team</A>.</P>
<H3>Directions</H3>
<P>You may upload a winzip, zip, or tar file to your website.  The contents of the archive should match the following directory tree structure, in other words the directories listed below should be the top level directories when the archive is created.</P>
<P>All files including files in zip and tar archive should not have spaces in their name.</P>
<P>Filenames can have mixed case and are not governed by an 8.3 filename name specification.
<P>If the file you are uploading is not a zip or tar archive, the file will be placed in the html directory for the website you specify.
<P>Allowable subdirectories in your archive file</P>
<UL>
<LI>html
<LI>images
</UL>
<P>NOTE: Do <b>NOT</B> put a subdirectory called cgi-bin in your archive file. This can damage the e-commerce engine at your website, if installed.</P>
<P>Example (Windows 9x Systems at MS-DOS prompt):</p>
cd C:\<BR>
mkdir website<BR>
cd C:\website<BR>
mkdir html<BR>
mkdir images<BR>
<P>Create all of your html files under html and put all of your gifs, jpegs, etc in the images directory and create appropriate relative links in you html files to the image files in images subdirectory.<p>
<p>zip all files under c:\website directory but do not zip the directory c:\website</p>

<P>If your archive has other directories in it besides the above mentioned names, these directories will not be accessed by the Clicktree.com server and will be merely wasting your websites disk space allotment.  This Site Maintenance Upload program does not check the integrity of your archive file so it is imperative that you specify your archive as mentioned above.  Future updates will verify the contents of the archive file you are uploading.</P>

<P>
<form action="/%s-cgi-bin/upload.pyc" method="POST" enctype="multipart/form-data">
<TABLE BORDER=0>
<TR><TD><B>Website Name</B>:</TD><TD><input name="website_name" type="text" size="50" maxlength="50"></TD></TR>
<TR><TD><B>Username</B>:</TD><TD><input name="username" type="text" size="9" maxlength="9"></TD></TR>
<TR><TD><B>Password:</B></TD><TD><input name="password" type="password" size="8" maxlength="8"></TD></TR>
<TR><TD><B>Archive filename</B>:</TD><TD><input name="archive" type="file" size="60"></TD></TR>
</TABLE>
<HR>
<input name="submit" type="submit" value="Upload Archive">
<p align="right"><A HREF="mailto:support@clicktree.com">Contact Support Team</a>
</form>
</body>
</html> 
""" % (upload_ceiling, declarations.store_info['db_name'])

if os.environ.has_key("HTTP_USER_AGENT"):
    browser = os.environ["HTTP_USER_AGENT"]
else:
    browser = "No Known Browser"

if os.environ.has_key("SCRIPT_NAME"):
    posturl = os.environ["SCRIPT_NAME"]
else:
    posturl = ""

form = cgi.FieldStorage()

if form.has_key("archive"):

    status, valid = authentication.password_valid(
        passwd_filename='/home/' + string.lower(string.strip(form['website_name'].value)) + '/admin/upload_passwd',
        crypt_salt=string.lower(string.strip(form['website_name'].value)),
        username=form['username'].value,
        password=form['password'].value)

    if status != 'success':
        html_msg = "Can not find password file for authentication of user.<BR>"
        email_msg = "Can not find password file for authentication of user."
        upload_results(html_msg, email_msg,form)
        sys.exit()
				
    if not valid:
        html_msg = "Invalid username or password specified.<BR>"
        email_msg = "Invalid username or password specified."
        upload_results(html_msg, email_msg, form)
        sys.exit()
		
    if not os.path.exists('/home/' + string.lower(string.strip(form['website_name'].value))):

        html_msg = "Upload site " + form['website_name'].value + " does not exist.<BR> No archive file was uploaded.<BR>"
        email_msg = "Upload site " + form['website_name'].value + " does not exist.\nNo archive file was uploaded.\n"
        
        upload_results(html_msg, email_msg, form)
        sys.exit()

    if form.has_key('archive'):
        # remove client's hard directory path from filename
        # to get just basename
        
        archive_size = len(form['archive'].value)
        
        if archive_size == 0:
            html_msg= "Suspicious archive file size of 0. Upload aborted.<BR>"
            upload_results(html_msg,'Suspicious archive file size of 0. Upload aborted.',form)
            sys.exit()
						
        if archive_size > upload_ceiling:
            html_msg = 'Archive file exceeds maximum upload allowed of %d bytes.<BR>' % (upload_ceiling)
            html_msg = html_msg + 'Archive file size is %d bytes.<BR>' % (archive_size)
            html_msg = html_msg + 'No archive file was uploaded.<BR>'

            email_msg = email_msg + 'Archive file exceeds maximum upload allowed of %d bytes.\n' % (upload_ceiling)
            email_msg = email_msg + 'Archive file size is %d bytes.\n' % (archive_size)
            email_msg = email_msg + 'No archive file was uploaded.\n'
            upload_results(html_msg, email_msg,form)
            sys.exit()
						
        archive_name = form['archive'].filename
        archive_name = string.lower(string.strip(archive_name))

        if string.rfind(archive_name,"\\") >= 0:
            archive_name = archive_name[string.rfind(archive_name,"\\")+1:]
        if string.rfind(archive_name,"/") >= 0:
            archive_name = archive_name[string.rfind(archive_name,"/")+1:]
        if string.rfind(archive_name,":") >= 0:
            archive_name = archive_name[string.rfind(archive_name,":")+1:]

        try:
            archive_file = open('/home/' + string.lower(string.strip(form['website_name'].value)) + '/' + archive_name, "wb")

        except IOError, exception_details:
            html_msg = "No permissions to upload file to the website %s. Uploaded aborted.<BR>" % (form['website_name'].value)
            
            upload_results(html_msg,'Archive file could not be uploaded to ' + form['website_name'].value + '.\nReason: ' + exception_details[1] + '\n\n',form)
            sys.exit()
						
        archive_file.write(form['archive'].value)
        archive_file.close()

        status, type_of_archive = os_utils.file_type('/home/' + string.lower(string.strip(form['website_name'].value)) + '/' + archive_name)

        if status == 'success':

            if type_of_archive == 'tar':

                os.chdir('/home/' + string.lower(string.strip(form['website_name'].value)))

                status, archive_output = os_utils.tar_extract('/home/' + string.lower(string.strip(form['website_name'].value)) + '/' +  archive_name, verbose=0)

            elif type_of_archive == 'zip' or type_of_archive == 'gzip':

                os.chdir('/home/' + string.lower(string.strip(form['website_name'].value)))
                
                if type_of_archive == 'zip':

                    status, archive_output = os_utils.unzip('/home/' + string.lower(string.strip(form['website_name'].value)) + '/' + archive_name, echoOnError=1)

                elif type_of_archive == 'gzip':

                    status, archive_output = os_utils.gunzip('/home/' + string.lower(string.strip(form['website_name'].value)) + '/' + archive_name, force=1, echoOnError=1)

                    if string.rfind(archive_name,".gz") >= 0:
                        tar_archive_name = archive_name[:string.rfind(archive_name,".gz")]

                    archive_name = tar_archive_name
										
                    status, type_of_archive = os_utils.file_type('/home/' + string.lower(string.strip(form['website_name'].value)) + '/' +  tar_archive_name)

                    if type_of_archive == 'tar':
                        
                        status, archive_output = os_utils.tar_extract('/home/' + string.lower(string.strip(form['website_name'].value)) + '/' +  tar_archive_name)
                        
                    else:
                        html_msg = 'Invalid archive file type.  Upload aborted.'
                        upload_results(html_msg,'Attempted upload to ' + form['website_name'].value + '.\nFailed since archive is an invalid type.',form)
                        sys.exit()

            elif type_of_archive == 'html' or type_of_archive == 'gif' or type_of_archive == 'jpeg':

                os.rename('/home/' + string.lower(string.strip(form['website_name'].value)) + '/' + archive_name, '/home/' + string.lower(string.strip(form['website_name'].value)) + '/html/' + archive_name)
                
                archive_name = 'html/' + archive_name
                
                status = 'success'
                archive_output = ''

            else:
                html_msg = 'Invalid archive file type.  Upload aborted.'
                upload_results(html_msg,'Attempted upload to ' + form['website_name'].value + '.\nFailed since archive is an invalid type.',form)
                sys.exit()
								
        else:
            html_msg = 'Invalid archive file type.  Upload aborted.'
            upload_results(html_msg,'Attempted upload to ' + form['website_name'].value + '.\nFailed since archive is an invalid type.',form)
            sys.exit()
						
        html_msg = '<TABLE BORDER=0>'

        if os.environ.has_key('REMOTE_ADDR'):
            html_msg = html_msg + '<TR><TD>Your IP Address:</TD><TD>%s</TD></TR>' % (os.environ['REMOTE_ADDR'])
            
        html_msg = html_msg + '<TR><TD>Your browser I.D.:</TD><TD><B>%s</B></TD></TR>' % (browser)
        html_msg = html_msg + '<TR><TD>Archive name is: </TD><TD>%s</TD></TR>' % (archive_name)
        html_msg = html_msg + '<TR><TD>Archive file size (bytes): </TD><TD>%s</TD></TR></TABLE>' % (os.stat('/home/' + string.lower(string.strip(form['website_name'].value)) + '/' + archive_name)[6])
        
        if type_of_archive == 'tar' or type_of_archive == 'zip':
            html_msg = html_msg + '<PRE>'
            html_msg = html_msg + archive_output
            html_msg = html_msg + '</PRE>'
            
        html_msg = html_msg + '<CENTER><B>Your archive file has been successfully uploaded and extracted.</B></CENTER>'
        html_msg = html_msg + '<HR><CENTER><FONT SIZE="-1"><A HREF="%s">Clicktree.com</A></FONT></CENTER>' % link

        email_msg = 'Archive file was uploaded to ' + form['website_name'].value + '.\nArchive file size (bytes): ' + `os.stat('/home/' + string.lower(string.strip(form['website_name'].value)) + '/' + archive_name)[6]` + '\n' + 'Archive filename: ' + archive_name + '\n' + archive_output + '\n'
        
        if type_of_archive == 'tar' or type_of_archive == 'zip':
            os.remove('/home/' + string.lower(string.strip(form['website_name'].value)) + '/' +  archive_name)

        upload_results(html_msg, email_msg, form)

        status, output = commands.getstatusoutput("chmod u=rwx,go= /home/%s/images" % (form['website_name'].value))
        status, output = commands.getstatusoutput("chmod u=rw,go= /home/%s/images/*" % (form['website_name'].value))
        status, output = commands.getstatusoutput("chmod u=rwx,go= /home/%s/html" % (form['website_name'].value))
        status, output = commands.getstatusoutput("chmod u=rw,go= /home/%s/html/*" % (form['website_name'].value))
        
    else:
        html_msg = "No file was received.  No archive filename was specified<BR>"
        upload_results(html_msg,'Attempted upload to ' + form['website_name'].value + '.\nFailed since archive filename was not specified.',form)
        
    print "</BODY></HTML>"

else:
    display_form(posturl)

