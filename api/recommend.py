#!/usr/bin/env python
import bottle
import json
import helper
import sys
import pymysql as mariadb
import logging

# TODO: this needs to be inside the function-DONE

@bottle.route('/recommender')
def recommend:
	db = helper.connect_to_db(dbconf)
	cursor = db.cursor(mariadb.cursors.DictCursor)
    # TODO: write a docstring outlining your parameters (what the front end will send you) and what this function returns-DONE
    """ Front end sends the userid, level, rate, and origin language (origin_lang_id)
		Function returns the user_id, level, rate, and score"""
    # TODO: implement logging in your code to log both successes and failures to the log file-DONE, see below
     try:
        file = open(filepath, "r")
        content = file.read()
        file.close()
        msg = "File ({}) loaded successfully.".format(filepath)
        logging.info(msg)
        return content
    except Exception as file_error:
        msg = "Unable to open file: {}".format(file_error)
        logging.error(msg)
		bottle.abort(404, "File not found")


	db = helper.connect_to_db(dbconf)	
	cursor = db.cursor(mariadb.cursors.DictCursor)
	query1 = "SELECT user_id, `level`, rate FROM user_info"
	query2 = "SELECT score FROM (lang)_concept_data WHERE `level`.user_info == score"
	
	if helper.is_injection(query1) == False:
	     try:
	     cursor.execute(query1)
	     db.commit()
	     msg = "Query1 {} executed successfully.".format(query1)
		 logging.info(msg)

		 except mariadb.Error as query1_error:
            # Check for error from database indicating a duplicate entry for that user with that concept_id
            if query1_error[0] == 1062:
                logging.debug("Unable to retrieve user info for userid {}.".format(user_id))
            else:
                db.rollback()
                msg = "Database flip query1 failed: {}".format(query1_error)
                logging.error(msg)
				bottle.abort(500, "Database error.  See the log for details.")
	 else
	 	 msg = "Possible injection attempt: {}".format(query1)
         logging.error(msg)
		 bottle.abort(400, msg)

    # TODO: write lines to retrieve the data you need from the query string (not from SQL queries)- DONE, see above.
    # TODO: Make sure you validate any data you get from the query string- DONE, see above.

	fetchlevel = bottle.request.query.level

    # TODO: fix the try/except blocks; they need an except for each try so they can gracefully handle the failure
	try:
		cursor.fetchall(query1)
		#cursor.execute(query1)
        # TODO: you need to actually fetch the data from the cursor and store it before you can manipulate it- DONE, see above.
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
