#!/usr/bin/env python

import csv
import sys
import pprint
import pymysql


# Function to convert a csv file to a list of dictionaries.  Takes in one variable called "variables_file"

def csv_dict_list(variables_file):
    # Open variable-based csv, iterate over the rows and map values to a list of dictionaries containing key/value pairs

    reader = csv.DictReader(open(variables_file, 'rb'))
    dict_list = []
    for line in reader:
        dict_list.append(line)
    return dict_list


def get_language(natual_position):
    # iterate through the natural position id and get the language

    # return the language to indiciate where to insert the data.
    return "eng_test"


def add_to_db(data):
    # Takes the data read in from csv file and adds it to the database

    # need to connect to the db
    try:
        conn = pymysql.connect(user='root', password='diglotbom2017', database='diglot')
        cursor = conn.cursor()
        pprint.pprint("Successfully Connected")
        try:
            insert_statement = ("INSERT INTO eng_test (master_position, natural_position, chunk_value, rank) "
                                "VALUES (%s, %s, %s, %s)")
            mp = ":01:01:01:001"
            np = "eng:01:01:01:001"
            text = "I, Nephi"
            rank = 1
            # for item in data:
                # need to read through the data
                # mp = item['master_position']
                # np = item['natural_position']
                # text = item['text']
                # rank = item['rank']
                # table = get_language(np)
                # need to write to the db
                #pprint.pprint(item)
            values = (mp, np, text, rank)
            pprint.pprint(values)
                #cursor.execute(insert_statement, data)
            cursor.execute(insert_statement, values)
            conn.commit()
            pprint.pprint(item)
            cursor.close()
        except pymysql.Error as error:
            return "Exception occurred: {}".format(error)
        conn.close()
        return "Success"
    except pymysql.Error as error1:
        return "Exception.occurred: {}".format(error1)


# Calls the csv_dict_list function, passing the named csv
device_values = csv_dict_list("diglot_test_data.csv")
# device_values = csv_dict_list(sys.argv[1])

# Prints the results nice and pretty like

# pprint.pprint(device_values)

add_to_db(device_values)

