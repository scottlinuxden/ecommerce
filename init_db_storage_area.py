#!/usr/bin/env python
# $Id: init_db_storage_area.py,v 1.2 2000/03/18 00:20:44 postgres Exp postgres 
# Copyright (C) 1999 LinuXden, All Rights Reserved
# Copright Statement at http://www.linuxden.com/copyrighted_apps.html
# 
import os, string, sys
import cgi, glob
import types
import commands

# to clean out an already existing db
# stop the postmaster
# rm -rf /var/lib/pgsql/*
# to initialize the database on a clean system or after 
# remove all db files
# start postmaster
# perform initdb --pglib=/usr/lib/pgsql

print "You will need the root password for your system"
print "to continue this install and be logged in as user postgres."
print ""

if getuser() != 'root':
	print 'You must be logged in as user root to'
	print 'initialize postgresql database storage area.'
	print 'Exiting application.'
	sys.exit(1)

os.putenv("PGLIB", "/usr/lib/pgsql")

os.putenv("PGDATA", "/var/lib/pgsql")

print "Do you want to delete all database(s) and"
print "initialize a postgresql db storage area,"
print 'This is a rather drastic thing to do all db data will'
print 'be deleted for good. (Y/N): ',

while 1:
	clean_and_create = sys.stdin.readline()
	if string.lower(string.strip(clean_and_create)) == 'y' or \
	   string.lower(string.strip(clean_and_create)) == 'n':
		break

if string.lower(string.strip(clean_and_create)) == 'y':
	status, output = commands.getstatusoutput('/etc/rc.d/init.d/postgresql stop')
	print output

	print 'Removing all file(s) under /var/lib/pgsql.'
	os.system("rm -rf /var/lib/pgsql/*")

	status, output = commands.getstatusoutput('/etc/rc.d/init.d/postgresql start')
	print output

	print 'Copying user authentication config file to storage area'

	# sets up configuration so all logins require a password
	os.system("cp -f /home/ecommerce/dbconfig/pg_hba.conf /var/lib/pgsql")

	print 'Initializing postgresql database storage area'
	
	os.system('initdb')
