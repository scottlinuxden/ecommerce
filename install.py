#!/usr/bin/env python
# $Id: install.py,v 1.9 2000/04/16 23:23:41 davis Exp davis $
# Copyright (C) 1999 LinuXden, All Rights Reserved
# Copright Statement at http://www.linuxden.com/copyrighted_apps.html
# 
import stat
import glob
import string
import compileall
import os_utils
import shutil
import os, string, sys
import cgi
import types
import commands
import getpass
import file_io
import ecommerce
from pg import DB
import authentication

class install:
	
	def __init__(self,
				 ignore_user_login=0,
				 prompt=1,
				 db_name=None,
				 domain_name=None,
				 postgres_username=None,
				 postgres_password=None,
				 db_admin_username=None,
				 db_admin_password=None,
				 visitor_username=None,
				 visitor_password=None,
				 help_url=None):
		
		self.db_name = db_name
		self.domain_name = domain_name
		self.postgres_username = postgres_username
		self.postgres_password = postgres_password
		self.db_admin_username = db_admin_username
		self.db_admin_password = db_admin_password
		self.visitor_username = visitor_username
		self.visitor_password = visitor_password
		self.help_url = help_url

		os.putenv("PGLIB", "/usr/lib/pgsql")

		os.putenv("PGDATA", "/var/lib/pgsql")

		if not ignore_user_login:

			if getpass.getuser() != 'postgres':
				print 'You must be logged in as user postgres to'
				print 'create a store db. Exiting application.'
				sys.exit(1)

		if prompt and db_name == None:

			while 1:
				print 'Enter the database name to manipulate: ',
				self.db_name = sys.stdin.readline()
				self.db_name = string.lower(string.strip(self.db_name[:-1]))
				if string.strip(self.db_name) != "":
					break
				else:
					print "You must enter a database name to manipulate"
					
		else:
			if db_name != None:
				self.db_name = string.lower(string.strip(db_name))

		if prompt and domain_name == None:

			while 1:
				print 'Enter the domain name for the store [EX. www.clicktree.com]: ',
				self.domain_name = sys.stdin.readline()
				self.domain_name = string.lower(string.strip(self.domain_name[:-1]))
				if string.strip(self.domain_name) != "":
					break
				else:
					print "You must enter a domain name for the store"
					
		else:
			if domain_name != None:
				self.domain_name = string.lower(string.strip(domain_name))

		if prompt and postgres_username == None:

			while 1:
				print "Enter the postgres username: ",
				self.postgres_username = sys.stdin.readline()
				self.postgres_username = string.lower(string.strip(self.postgres_username[:-1]))
				if string.strip(self.postgres_username) != "":
					break
				else:
					print "You must enter a postgres username"

		else:
			if postgres_username != None:
				self.postgres_username = string.lower(string.strip(postgres_username))

		if prompt and postgres_password == None:

			while 1:
				self.postgres_password = getpass.getpass(prompt='Enter the password for the postgres user: ')
				
				if string.strip(self.postgres_password) != "":
					os.putenv("PGPASSWORD", self.postgres_password)
					break
				else:
					print "You must enter a password"

		else:
			if postgres_password != None:
				self.postgres_password = postgres_password

		if prompt and db_admin_username == None:
			while 1:
				
				print "Enter the db admin username: ",
				self.db_admin_username = sys.stdin.readline()
				self.db_admin_username = string.lower(string.strip(self.db_admin_username[:-1]))
				if string.strip(self.db_admin_username) != "":
					break
				else:
					print "You must enter a username"

		else:
			if db_admin_username != None:
				self.db_admin_username = string.lower(string.strip(db_admin_username))
				
		if prompt and db_admin_password == None:
			
			while 1:
				self.db_admin_password = getpass.getpass(prompt='Enter the password for the db admin: ')
				
				if string.strip(self.db_admin_password) != "":
					break
				else:
					print "You must enter a password"
					
		else:
			if db_admin_password != None:
				self.db_admin_password = db_admin_password
				
		if prompt and visitor_username == None:
			while 1:
				
				print "Enter the site visitor username: ",
				self.visitor_username = sys.stdin.readline()
				self.visitor_username = string.lower(string.strip(self.visitor_username[:-1]))
				if string.strip(self.visitor_username) != "":
					break
				else:
					print "You must enter a username"
					
		else:
			if visitor_username != None:
				self.visitor_username = string.lower(string.strip(visitor_username))
				
		if prompt and visitor_password == None:
			while 1:
				
				self.visitor_password = getpass.getpass(prompt='Enter the password for the site visitor: ')
				
				if string.strip(self.visitor_password) != "":
					break
				else:
					print "You must enter a password"
					
		else:
			if visitor_password != None:
				self.visitor_password = visitor_password
				
		if prompt and help_url == None:
			while 1:
				
				print "Enter the URL for your store's help documentation: ",
				self.help_url = sys.stdin.readline()
				self.help_url = string.lower(string.strip(self.help_url[:-1]))
				if string.strip(self.help_url) != "":
					break
				else:
					print "You must enter a URL for your store's help documentation"
					
		else:
			if help_url != None:
				self.help_url = string.lower(string.strip(help_url))

	def create_declarations(self):

		status, declaration_template_lines = file_io.readFromFile('declarations.template')
		
		line_index = 0
		
		for line in declaration_template_lines:
			
			field = string.split(line)

			if len(field) < 3:
				line_index = line_index + 1
				continue

			if field[0][:10] == "store_info":

				if field[1] == '=':
					
					if field[2] == "'{{{STORE_DB_NAME}}}'":
						declaration_template_lines[line_index] = field[0] + ' ' + field[1] + " '" + self.db_name + "'"

					elif field[2] == "'{{{STORE_DOMAIN_NAME}}}'":
						declaration_template_lines[line_index] = field[0] + ' ' + field[1] + " '" + self.domain_name + "'"
						
					elif field[2] == "'{{{STORE_BROWSER_USERNAME}}}'":
						declaration_template_lines[line_index] = field[0] + ' ' + field[1] + " '" + self.visitor_username + "'"
						
					elif field[2] == "'{{{STORE_BROWSER_PASSWORD}}}'":
						declaration_template_lines[line_index] = field[0] + ' ' + field[1] + " '" + self.visitor_password + "'"
						
					elif field[2] == "'{{{STORE_HELP_URL}}}'":
						declaration_template_lines[line_index] = field[0] + ' ' + field[1] + " '" + self.help_url + "'"
						
			line_index = line_index + 1

		status, output = file_io.writeToFile('declarations.py', declaration_template_lines)

	def create_db(self):

		import declarations

		os.system('destroydb %s' % (self.db_name))
		os.system("createdb %s" % (self.db_name))
		
		os.system("/usr/bin/destroyuser " + self.db_admin_username)
		
		print "Answer NO to the next prompt"
		
		os.system("/usr/bin/createuser -i 1000 -D -U " + self.db_admin_username)
		
		os.system("/usr/bin/destroyuser " + self.visitor_username)
		
		print "Answer NO to the next prompt"
		
		os.system("/usr/bin/createuser -i 2000 -D -U " + self.visitor_username)
		
		dbResult = ecommerce.connectDB(self.postgres_username, self.postgres_password, self.db_name)
				
		if dbResult['status'] != "success":
			print dbResult['message']
			sys.exit(1)

		db = dbResult['result']

		queryResult = ecommerce.executeSQL(db, "DELETE FROM pg_group WHERE groname = 'admins'")
		
		queryResult = ecommerce.executeSQL(db, 
										   "INSERT INTO pg_group (groname, grosysid, grolist) VALUES ('admins', '1', '{1000}')")
		
		if queryResult["status"] != 'success':
			print queryResult["status"]
			sys.exit(1)
	
		queryResult = ecommerce.executeSQL(db, "DELETE FROM pg_group WHERE groname = 'users'")
	
		queryResult = ecommerce.executeSQL(db, 
										   "INSERT INTO pg_group (groname, grosysid, grolist) VALUES ('users', '2', '{2000}')")
		
		if queryResult["status"] != 'success':
			print queryResult["status"]
			sys.exit(1)

		queryResult = ecommerce.executeSQL(db, "ALTER USER postgres WITH PASSWORD " + self.postgres_password)

		if queryResult["status"] != 'success':
			print queryResult['message']
			sys.exit(1)

		queryResult = ecommerce.executeSQL(db, "ALTER USER %s WITH PASSWORD %s IN GROUP admins" % (self.db_admin_username, self.db_admin_password))

		if queryResult["status"] != 'success':
			print queryResult['message']
			sys.exit(1)

		queryResult = ecommerce.executeSQL(db, "ALTER USER %s WITH PASSWORD %s IN GROUP users" % (self.visitor_username, self.visitor_password))

		if queryResult["status"] != 'success':
			print queryResult['message']
			sys.exit(1)

		queryResult = ecommerce.create_tables(db, declarations.define_tables(), 1)

		if queryResult["status"] != 'success':
			print queryResult['message']
			sys.exit(1)

		status, populate_tables = file_io.readFromFile(self.db_name + '.tables')

		for index in xrange(0,len(populate_tables)):
			populate_tables[index] = string.strip(populate_tables[index])
			if populate_tables[index] == '':
				del populate_tables[index]
			elif populate_tables[index][:4] == 'COPY':
				populate_tables[index] = os.path.expandvars(populate_tables[index])
				
		queryResult = ecommerce.executeSqlItemList(db, populate_tables, 1,1)

		if queryResult["status"] != 'success':
			print queryResult
			print "Failed to execute all populate table statements"
			sys.exit(1)

		grantList = []

		privileges = declarations.table_privileges()
		
		for table_name in privileges.keys():
			for user_name in privileges[table_name].keys():
				grantStatement = "GRANT "
				for privilege in privileges[table_name][user_name]:
					grantStatement = grantStatement + privilege + ", "
					
				grantStatement = grantStatement[:-2] + " ON " + table_name + " TO " + user_name
				grantList.append(grantStatement)
								
			# grant all privileges to the db admin
			grantList.append("GRANT ALL ON " + table_name + " TO " + self.db_admin_username)

		queryResult = ecommerce.executeSqlItemList(db, grantList, 1)

		if queryResult["status"] != 'success':
			print "Failed to execute all GRANTS"
			sys.exit(1)

	def create_authentication_files(self):

		status, output = authentication.add_pwd_entry('upload_passwd', self.db_name, self.db_admin_username, self.db_admin_password)
		status, output = authentication.add_pwd_entry('clean_passwd', self.db_name, self.db_admin_username, self.db_admin_password)

	def ecommerce_web(self):

		dist_list = [
			'authentication.py',
			'os_utils.py',
			'upload.py',
			'Cookie.py',
			'clean_site.py',
			'customer_admin.py',
			'customer_property_admin.py',
			'declarations.py',
			'ecommerce.py',
			'feedback.py',
			'file_io.py',
			'market_status_values_admin.py',
			'order_admin.py',
			'order_status_values_admin.py',
			'payment_methods_admin.py',
			'product_admin.py',
			'product_categories_admin.py',
			'property_admin.py',
			'sales_tax_admin.py',
			'shipping_methods_admin.py',
			'site_usage.py',
			'store.py',
			'store_admin.py',
			'time_pkg.py',
			'view_properties.py']
		
		store_name = self.db_name

		if not os.path.exists(os.path.join('/home', store_name)):
			os.mkdir(os.path.join('/home', store_name))

		if not os.path.exists(os.path.join('/home', store_name, 'html')):
			os.mkdir(os.path.join('/home', store_name, 'html'))

		if not os.path.exists(os.path.join('/home', store_name, 'cgi-bin')):
			os.mkdir(os.path.join('/home', store_name, 'cgi-bin'))

		if not os.path.exists(os.path.join('/home', store_name, 'images')):
			os.mkdir(os.path.join('/home', store_name, 'images'))

		if not os.path.exists(os.path.join('/home', store_name, 'admin')):
			os.mkdir(os.path.join('/home', store_name, 'admin'))

		if os.path.exists(os.path.join('.', 'staging')):
			os_utils.super_remove(os.path.join('.', 'staging'))

		os.mkdir(os.path.join('.', 'staging'))

		for curfile in dist_list:
			shutil.copy(curfile,os.path.join('.','staging'))

		os.chdir(os.path.join('.','staging'))

		compileall.compile_dir('.',0,None,0)
		
		os.chdir(os.path.join('..'))
		
		for curfile in glob.glob(os.path.join('.','staging','*.pyc')):
			shutil.copy(curfile,os.path.join('/home',store_name,'cgi-bin'))

		shutil.copy(os.path.join('images','imageMissing.gif'),os.path.join('/home',store_name,'images'))

		os_utils.set_file_mode(filename = os.path.join('/home',store_name),
							   user = ['r','w','x'])

		os_utils.set_file_mode(filename = os.path.join('/home',store_name,'html'),
							   user = ['r','w','x'])
		
		for curfile in glob.glob(os.path.join('/home',store_name,'html','*')):
			os_utils.set_file_mode(filename = curfile,
								   user = ['r','w'])

		os_utils.set_file_mode(filename = os.path.join('/home',store_name,'cgi-bin'),
							   user = ['r','x'])

		for curfile in glob.glob(os.path.join('/home',store_name,'cgi-bin','*')):
			os_utils.set_file_mode(filename = curfile,
								   user = ['r','x'])

		os_utils.set_file_mode(filename = os.path.join('/home',store_name,'images'),
							   user = ['r','w','x'])

		for curfile in glob.glob(os.path.join('/home',store_name,'images','*')):
			os_utils.set_file_mode(filename = curfile,
								   user = ['r','w'])

		os_utils.set_file_mode(filename = os.path.join('/home',store_name,'admin'),
							   user = ['r','w','x'])

		if not os.path.exists(os.path.join('/home',store_name,'admin','upload_passwd')):
			if os.path.exists('upload_passwd'):
				shutil.copy('upload_passwd',os.path.join('/home',store_name,'admin'))
				os.remove('upload_passwd')
			else:
				print '\nError: an upload password file does not exist'
				print 'If you do not create an upload password file'
				print 'users will not be able to upload files.'
				
		for curfile in glob.glob(os.path.join('/home',store_name,'admin','*')):
			os_utils.set_file_mode(
				filename = curfile,
				user = ['r','w'])

		status, output = os_utils.super_chown(
			directory_name=os.path.join('/home',store_name),
			username='nobody',
			groupname='nobody')

		if status != 'success':
			print 'Ownership settings of store directory tree %s failed.' % (os.path.join('/home',store_name))

	def su_exec_ecommerce_web(self):
		os_utils.su_exec(command = 'python install_web.py %s' % (self.db_name))
				
if __name__ == "__main__":

	install_engine = install()
	install_engine.create_declarations()
	install_engine.create_db()
	install_engine.create_authentication_files()
	install_engine.su_exec_ecommerce_web()
