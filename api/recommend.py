#!/usr/bin/env python
import bottle
import json
import helper
import sys
import pymysql as mariadb
import logging

db = helper.connect_to_db(dbconf)
cursor = db.cursor(mariadb.cursors.DictCursor)

@bottle.route('/recommender')
def recommend:

	query1 = "SELECT user_id, level, rate FROM user_info"
	query2 = "SELECT score FROM (lang)_concept_data WHERE level.user_info == score"
	
	if helper.check_login = True #This helper thing to call in the user login info
		fetchlevel = bottle.request.query.level

		try:
			cursor.execute(query1)#Run query1
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
