#!/usr/bin/env python
# $Id: install_web.py,v 1.2 2000/04/06 00:31:13 davis Exp $
# Copyright (C) 1999 LinuXden, All Rights Reserved
# Copright Statement at http://www.linuxden.com/copyrighted_apps.html
# 
import install
import sys

def main():
	install_engine = install.install(ignore_user_login=1,prompt=0,db_name=sys.argv[1])
	install_engine.ecommerce_web()

if __name__ == "__main__":
	main()
