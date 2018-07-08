#!/usr/bin/env python
# $Id: create_db.py,v 1.7 2000/04/06 00:31:13 davis Exp $
# Copyright (C) 1999 LinuXden, All Rights Reserved
# Copright Statement at http://www.linuxden.com/copyrighted_apps.html
# 
import install

def main():
	install_engine = install.install()
	install_engine.create_declarations()
	install_engine.create_db()

if __name__ == "__main__":
	main()
