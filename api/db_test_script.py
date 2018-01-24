#!/usr/bin/env python

import csv
import sys
import pprint
import pymysql as mariadb


# Function to convert a csv file to a list of dictionaries.  Takes in one variable called "variables_file"

def csv_dict_list(variables_file):
    # Open variable-based csv, iterate over the rows and map values to a list of dictionaries containing key/value pairs

    reader = csv.DictReader(open(variables_file, 'rb'))
    dict_list = []
    for line in reader:
        dict_list.append(line)
    return dict_list


def get_language(natual_position):
	#iterate through the natural position id and get the language

	#return the language to indiciate where to insert the data.
	return "eng_test"


def add_to_db(data):
	#Takes the data read in from csv file and adds it to the database

	#need to connect to the db
	try:
		db = mariadb.connect(user='diglotadmin', password='CYn8-T#qZ6-.8!@2', database='diglot')
		cursor = db.cursor()
		try:
			for item in data:
				#need to read through the data
				mp = item['master_position']
				np = item['natural_position']
				text = item['text']
				rank = item['rank']
				table = get_language(np)
				#need to write to the db
				cursor.execute("INSERT INTO " + table + " (master_position, natural_position, chunk_value, rank) VALUES (%s, %s, %s, %i)", (mp, np, text, rank))
				query_result = cursor.fetchall()
        		
    		cursor.close()
		except maradb.Error as error:
	except mariadb.Error as error1:

	connection.close()

# Calls the csv_dict_list function, passing the named csv
device_values = csv_dict_list("diglot_test_data.csv")
# device_values = csv_dict_list(sys.argv[1])

# Prints the results nice and pretty like

pprint.pprint(device_values)

add_to_db(device_values)

pprint.pprint("Successfully added the data")