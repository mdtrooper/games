#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from getopt import *
import json
import pystache

# Debug
from pprint import *

def help():
	print("Converter list games in json to github markdown.\n")
	print("Usage:")
	print("\t -o <file>, --output <file> \t Set the output file")
	print("\t -t <file>, --template <file> \t Set the template file (in mustache syntax)")
	print("\t -d <file>, --data <file> \t Set the data file (in json syntax)")
	print("\t -h, --help \t\t\t Show this help")

def get_categories(data):
	categories = set()
	
	for game in data['games']:
		categories.add(game['category'])
	
	categories = list(categories)
	
	return categories

def get_systems(data):
	systems = set()
	
	for game in data['games']:
		systems.add(game['system'])
	
	systems = list(systems)
	
	return systems

def is_any_game_with_category_and_system(data, category, system):
	return_var = False
	
	for game in data['games']:
		if game['category'] == category and game['system'] == system:
			return_var = True
			break
	
	return return_var

def main():
	try:
		options, args = getopt(sys.argv[1:], 'o:t:d:h', \
			['output=', 'template=', 'data=', 'help'])
	except GetoptError as err:
		print("[FAIL] " + err)
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
	
	if (not template_file) or (not data_file):
		print("[FAIL] Template files is not setted and data file is not setted.")
		help()
		exit(1)
	
	print("[INFO] Starting to parse the data file.")
	
	json_data=open(data_file)
	try:
		data = json.load(json_data)
	except ValueError as err:
		print("[FAIL] There is a error in the data file (%s)." % data_file)
		print err
		exit(1)
	
	categories = get_categories(data)
	categories.sort()
	systems = get_systems(data)
	systems.sort()
	
	print("[INFO] Making the intermediate json for the mustache template.")
	intermediate_json = {}
	intermediate_json['toc'] = []
	for system in systems:
		item = {}
		item['system'] = system
		item['category_toc'] = []
		
		for category in categories:
			if is_any_game_with_category_and_system(data, category, system):
				item2 = {}
				item2['category'] = category
				item2['mardown_anchor(category)'] = category
				item['category_toc'].append(item2)
		
		intermediate_json['toc'].append(item)
	
	pprint(intermediate_json)
	
	print("[INFO] Render the template.")
	
	renderer = pystache.Renderer()
	print renderer.render_path(template_file, intermediate_json)

if __name__ == "__main__":
	main()