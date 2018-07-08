# $Id: file_io.py,v 1.5 2000/04/06 00:31:13 davis Exp $ 
# Copyright (C) 1999 LinuXden, All Rights Reserved
# Copright Statement at http://www.linuxden.com/copyrighted_apps.html
# 
import os
import sys
import string
import fileinput

def readFromFile(filename):
	try:
		outputFile = open(filename, 'r')
	except IOError, exception_details:
		return('error: Can not open file: ' + filename + ', Reason:' + exception_details[1], None)
		
	data = outputFile.readlines()
		
	# chop off carriage return from data line if it is there
	for i in xrange(0,len(data)):
		if data[i][-1:] == '\n':
			data[i] = data[i][:-1]
	outputFile.close()
	return ('success', data)

def writeToFile(filename,data):
	try:
		outputFile = open(filename, 'w')
	except IOError, exception_details:
		return('error: Can not open file: ' + filename + ', Reason:' + exception_details[1], None)

	for i in xrange(0,len(data)):
		outputFile.write(data[i] + '\n')
	outputFile.close()

	return ('success', None)
