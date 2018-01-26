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
    #iterate through the natural position id and get the language

    #return the language to indicate where to insert the data.
    return "eng_test"


def add_to_db(data):
    #Takes the data read in from csv file and adds it to the database

    #need to connect to the db
    global insert_error
    try:
        con = pymysql.connect(host='localhost', user='diglotadmin', password='CYn8-T#qZ6-.8!@2', database='diglot', use_unicode=True, charset='utf8')
        cursor = con.cursor()
        try:
            for item in data:
                #need to read through the data
                mp = item['master_position']
                np = item['natural_position']
                text = item['text']
                rank = item['rank']
                table = get_language(np)
                #need to write to the db
                insert_statement = "INSERT INTO " + table + "(master_position, natural_position, chunk_value, rank) " \
                                                            "VALUES (%s, %s, %s, %s); "
                values = (mp, np, text, rank)
                try:
                    cursor.execute(insert_statement, values)
                    con.commit()
                    print_statement = values + ": Was successfully added to the database."
                    pprint.pprint(print_statement)
                    return "Success"
                except pymysql.Error as insert_error:
                    pprint.pprint(insert_error)
                    return "Exception.occurred: {}".format(insert_error)
            con.close()
            pprint.pprint("Successfully added the data from the csv file")
            return "Success"
        except pymysql.Error as forloop_error:
            pprint.pprint(forloop_error)
            return "Exception.occurred: {}".format(forloop_error)
        pprint.pprint("The script has finish adding data to the database")
        return "Success"
    except pymysql.Error as connection_error:
        pprint.pprint(connection_error)
        return "Exception.occurred: {}".format(connection_error)


# Calls the csv_dict_list function, passing the named csv
data_values = csv_dict_list("eng_test.csv")
# device_values = csv_dict_list(sys.argv[1])

# Prints the results nice and pretty like

pprint.pprint(data_values)

add_to_db(data_values)

pprint.pprint("Successfully added the data")