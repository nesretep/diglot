#!/usr/bin/env python3
import bottle
import json
import helper
import sys
import pymysql as mariadb
import logging

sys.path.extend(['/git/diglot/api'])
dbconf = "conf/diglot.conf"

@bottle.route('/recommender')
def recommend():
    """
    Sends to the front end the next group of concepts to auto-flip for the user based on the user's level and rate
    Parameters will be send via a query string in the API call

    :param user_id: (str converted to int) user id number of the user getting the recommendations
    :return:
    """
    try:
        user_id = int(bottle.request.query.user_id)
    except ValueError as uid_faliure:
        msg = "Invalid user_id ({}) passed in API call.".format(bottle.request.query.user_id)
        logging.error(msg)
        bottle.abort(400, "Check the log for details.")

    # If API will get sent this info below, we need the lines to grab them and validate the info
    if helper.is_valid_lang(bottle.request.query.lang):
        lang = bottle.request.query.lang
    else:
        msg = "Invalid language identifier ({}) for origin language.".format(bottle.request.query.lang)
        logging.error(msg)
        bottle.abort(400, msg)

    try:
        level = int(bottle.request.query.level)
    except ValueError as uid_faliure:
        msg = "Invalid level ({}) passed in API call.".format(bottle.request.query.level)
        logging.error(msg)
        bottle.abort(400, "Check the log for details.")

    try:
        rate = int(bottle.request.query.rate)
    except ValueError as uid_faliure:
        msg = "Invalid rate ({}) passed in API call.".format(bottle.request.query.rate)
        logging.error(msg)
        bottle.abort(400, "Check the log for details.")

    db = helper.connect_to_db(dbconf)
    cursor = db.cursor(mariadb.cursors.DictCursor)

    # If we aren't getting sent the lang, rate, and level in the API call we'll need to query for it
    # We may need different queries
    query1 = "SELECT `level`, rate, lang FROM user_info WHERE user_id = %s"

    if helper.is_injection(query1) == False:
        try:
            cursor.execute(query1, (user_id,))
            query1_result = cursor.fetchall()
            msg = "Query1 {} executed successfully.".format(query1)
            logging.info(msg)
            db.close()
            return json.dumps(query1_result)
        except mariadb.Error as query1_error:
            msg = "Recommend query1 failed: {}".format(query1_error)
            logging.error(msg)
            db.close()
            bottle.abort(500, "Database error.  See the log for details.")




