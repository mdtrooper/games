#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from getopt import *
import json
import pystache

# Debug
from pprint import *

def help():
	print("Converter list games in json to github markdown\n")
	print("Usage:")
	print("\t -o <file>, --output <file> \t Set the output file")
	print("\t -t <file>, --template <file> \t Set the template file (in mustache syntax)")
	print("\t -d <file>, --data <file> \t Set the data file (in json syntax)")
	print("\t -h, --help \t\t\t Show this help")

def main():
	try:
		options, args = getopt(sys.argv[1:], 'o:t:d:h', \
			['output=', 'template=', 'data=', 'help'])
	except GetoptError as err:
		print(err)
		help()
		sys.exit(2)
	
	output_file = None
	template_file = None
	data_file = None
	if args:
		data_file = args[0]
	
	for opt, val in options:
		if opt in ("-h", "--help"):
			help()
			sys.exit(0)
		
		if opt in ("-o", "--output"):
			output_file = val
		elif opt in ("-t", "--template"):
			template_file = val
		elif opt in ("-d", "--data"):
			data_file = val
	
	

if __name__ == "__main__":
	main()