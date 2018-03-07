#!/usr/bin/env python
import bottle
import json
import helper
import sys
import pymysql as mariadb
import logging

# TODO: this needs to be inside the function
db = helper.connect_to_db(dbconf)
cursor = db.cursor(mariadb.cursors.DictCursor)

@bottle.route('/recommender')
def recommend:
    # TODO: write a docstring outlining your parameters (what the front end will send you) and what this function returns
    # TODO: implement logging in your code to log both successes and failures to the log file
	query1 = "SELECT user_id, `level`, rate FROM user_info"
	query2 = "SELECT score FROM (lang)_concept_data WHERE `level`.user_info == score"
	
    # TODO: write lines to retrieve the data you need from the query string (not from SQL queries)
	fetchlevel = bottle.request.query.level

    # TODO: fix the try/except blocks; they need an except for each try so they can gracefully handle the failure
	try:
		cursor.execute(query1)#Run query1
        # TODO: you need to actually fetch the data from the cursor and store it before you can manipulate it
        # Use cursor.fetchone() or cursor.fetchall()
		query1_result = level + 1 #Add 1 to the user level
		return json.dumps(query_result1) #JSON-ify the result from query
		level = query_result1 #updates user score
		for query1_result #For that updated score
			cursor.execute(query2) #Query the db for the words where the new user score = level
		cursor.close()
		db.close()

	try:
		cursor.execute(query1)
		#***Send request for the number of recommended words***
		query1_result = score
		return json.dumps(query1_result)
		#***Send the queried data back to the front end for which words to recommend***
		cursor.close()
		db.close()
