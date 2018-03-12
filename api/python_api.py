#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: python_api.py
# Python REST API for the Diglot Book of Mormon web app

import bottle
import json
import helper
import sys
import pymysql as mariadb
import logging

sys.path.extend(['/git/diglot/api'])

books = {"1Nephi": "01", "2Nephi": "02", "Jacob": "03", "Enos": "04", "Jarom": "05",
         "Omni": "06", "Words of Mormon": "7", "Mosiah": "08", "Alma": "09", "Helaman": "10",
         "3Nephi": "11", "4Nephi": "12", "Mormon": "13", "Ether": "14", "Moroni": "15"}

dbconf = "conf/diglot.conf"


@bottle.route('/')
def start(filepath="../login.html"):
    """
    Loads the page defined in the query string as "page"

    :param filepath: (str) filename set by default; may be overridden
    :return content: (str) the contents of the html page specified
    """
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


@bottle.route('/main')
def load_main(filename="../index.html"):
    """
    Loads the main page showing the Book of Mormon text.

    :param filename: (str) URL to load; defaults to the path specified above
    :return content: contents of the file loaded
    """
    uid = bottle.request.query.uid

    try:
        file = open(filename, "r")
        content = file.read()
        file.close()
        return content
    except IOError as file_error:
        msg = "Unable to open file: {}".format(file_error)
        logging.error(msg)
        bottle.abort(404, "File not found")


@bottle.route('/login')
def load_login_page(filename="../login.html"):
    """
    Loads the login page.

    :param filename: (str) URL to load; defaults to the path specified above
    :return content: contents of the file loaded
    """
    try:
        file = open(filename, "r")
        content = file.read()
        file.close()
        return content
    except IOError as file_error:
        msg = "Unable to open file: {}".format(file_error)
        logging.error(msg)
        bottle.abort(404, "File not found")


@bottle.get('/<lang>/<book>/<chapter>')
def get_chapter(lang, book, chapter):
    """
    To return all chunks for the given chapter in JSON format

    :param lang: (str) 3 character ISO 639-3 designation for the language
    :param book: (str) the book requested as an integer indicating the order it appears in the Book of Mormon
    :param chapter: (str) the chapter in the book requested
    :param critical: (str) boolean as int that shows if we are at/past the critical point
    :return: JSON-ified dict containing a list Instances for the chapter requested
    """
    chap_uid = "{}:{}:{}{}".format(lang, book, chapter, "%")
    db = helper.connect_to_db(dbconf)
    cursor = db.cursor(mariadb.cursors.DictCursor)

    query = "SELECT origin.instance_id, origin.master_position, origin.instance_text, con.concept_id FROM {} AS origin \
             LEFT JOIN {}_concept AS con ON origin.chunk_id = con.chunk_id WHERE origin.instance_id LIKE %s \
             ORDER BY origin.instance_id".format(lang, lang)

    try:
        cursor.execute(query, (chap_uid,))
        query_result = cursor.fetchall()
        cursor.close()
        msg = "Query {} executed successfully.".format(query)
        logging.info(msg)
        db.close()
        return json.dumps(query_result)
    except mariadb.Error as query_error:
        msg = "Database query failed: {}".format(query_error)
        logging.error(msg)
        db.close()
        bottle.abort(500, "Database error.  See the log for details.")

# @bottle.route('/cp')
def critical_get_chapter():
    """
    To return all chunks for the given chapter in JSON format after reaching the critical point
    Parameters are passed to the function via a query string

    :param lang: (str) 3 character ISO 639-3 designation for the origin language
    :param target_lang: (str) 3 character ISO 639-3 designation for the target language
    :param book: (str) the book requested as an integer indicating the order it appears in the Book of Mormon
    :param chapter: (str) the chapter in the book requested
    :return: JSON-ified dict containing a list Instances for the chapter requested
    """
    if helper.is_valid_lang(bottle.request.query.lang):
        lang = bottle.request.query.lang
    else:
        msg = "Invalid language identifier ({}) for origin language.".format(bottle.request.query.lang)
        logging.error(msg)
        bottle.abort(400, msg)

    if helper.is_valid_lang(bottle.request.query.target_lang):
        target_lang = bottle.request.query.target_lang
    else:
        msg = "Invalid language identifier ({}) for target language.".format(bottle.request.query.target_lang)
        logging.error(msg)
        bottle.abort(400, msg)

    try:
        book = int(bottle.request.query.book)
        chapter = int(bottle.request.query.chapter)
    except ValueError as convert_error:
        msg = "Invalid value given for book or chapter: {}".format(convert_error)
        logging.error(msg)
        bottle.abort(400, msg)

    chap_uid = "{}:{}:{}{}".format(target_lang, book, chapter, "%")

    db = helper.connect_to_db(dbconf)
    cursor = db.cursor(mariadb.cursors.DictCursor)

    query = "SELECT target.instance_id AS target_instance_id, target.master_position AS target_master_position, \
             target.instance_text AS target_instance_text, origin_concept.concept_id AS origin_concept_concept_id \
             FROM {} AS target LEFT JOIN {} AS origin ON target.master_position = origin.master_position \
             LEFT JOIN {}_concept AS origin_concept ON orign.chunk_id = origin_concept.chunk_id \
             WHERE target.instance_id LIKE '{}' ORDER BY target.instance_id".format(target_lang, lang, lang, chap_uid)

    try:
        cursor.execute(query, (chap_uid,))
        query_result = cursor.fetchall()
        cursor.close()
        msg = "Query {} executed successfully.".format(query)
        logging.info(msg)
        db.close()
        return json.dumps(query_result)
    except mariadb.Error as query_error:
        msg = "Database query failed: {}".format(query_error)
        logging.error(msg)
        db.close()
        bottle.abort(500, "Database error.  See the log for details.")


@bottle.route('/flip')
def flip_one_concept():
    """
    Sends data for switching an instance to the target language.  Sets one Instance as flipped in the database.
    Parameters are retrieved from the query string of the HTTP request

    :param concept_id: (str) concept identifier for the concept to be flipped
    :param current_pos: (str) current position in the text
    :param user_id: (str) id of the user for which the concept is being flipped
    :param target_lang: (str) 3 character ISO 639-3 designation for the target language
    :return query2_result: JSON-ified dict containing the instance requested for the flip
    """
    # Validating/Sanitizing data for the query
    if helper.is_valid_lang(bottle.request.query.target_lang):
        target_lang = bottle.request.query.target_lang
    else:
        msg = "Invalid language identifier ({}) for target language.".format(bottle.request.query.target_lang)
        logging.error(msg)
        bottle.abort(400, msg)

    if helper.is_valid_concept(bottle.request.query.concept_id):
        concept_id = bottle.request.query.concept_id
    else:
        msg = "Invalid concept identifier ({})."
        logging.error(msg)
        bottle.abort(400, msg)

    if helper.is_valid_lang(concept_id[:3]):
        lang = concept_id[:3]
    else:
        msg = "Invalid language identifier ({}) for origin language.".format(concept_id[:3])
        logging.error(msg)
        bottle.abort(400, msg)

    if helper.is_valid_uid(bottle.request.query.current_pos, "cp"):
        current_pos = bottle.request.query.current_pos
    else:
        msg = "Invalid current position identifier ({}).".format(bottle.request.query.current_pos)
        logging.error(msg)
        bottle.abort(400, msg)

    try:
        user_id = int(bottle.request.query.user_id)
    except ValueError as convert_error:
        msg = "Invalid user_id ({}): {}".format(user_id, convert_error)
        logging.error(msg)
        bottle.abort(400, msg)

    # Query database for chunk
    db = helper.connect_to_db(dbconf)
    cursor = db.cursor(mariadb.cursors.DictCursor)

    query1 = "INSERT INTO flipped_list (user_id, concept_id) VALUES ('{}', '{}')".format(user_id, concept_id)
    if helper.is_injection(query1) == False:
        try:
            cursor.execute(query1)
            db.commit()
            msg = "Query1 {} executed successfully.".format(query1)
            logging.info(msg)
        except mariadb.Error as query1_error:
            # Check for error from database indicating a duplicate entry for that user with that concept_id
            if query1_error[0] == 1062:
                logging.warning("Instance already in flipped_list for user_id {}.".format(user_id))
            else:
                db.rollback()
                msg = "Database flip query1 failed: {}".format(query1_error)
                logging.error(msg)
                bottle.abort(500, "Database error.  See the log for details.")
    else:
        msg = "Possible injection attempt: {}".format(query1)
        logging.error(msg)
        bottle.abort(400, msg)
    # Grabs the info needed on the front end to complete the flipping of the concept
    # TODO: fix SQL query around LIKE
    query2 = "SELECT origin.instance_id AS origin_instance_id, target.instance_id AS target_instance_id, \
              target.instance_text AS target_instance_text FROM {}_concept AS con INNER JOIN {} AS origin ON \
              origin.chunk_id = con.chunk_id INNER JOIN {} AS target ON origin.master_position = target.master_position \
              WHERE con.concept_id = '{}' AND origin.instance_id LIKE '{}{}' \
              ORDER BY origin.instance_id".format(lang, lang, target_lang, concept_id, current_pos, "%")
    if helper.is_injection(query2) == False:
        try:
            cursor.execute(query2)
            query2_result = cursor.fetchall()
            msg = "Query2 {} executed successfully.".format(query2)
            logging.info(msg)
            db.close()
            return json.dumps(query2_result)
        except mariadb.Error as query2_error:
            msg = "Database flip query2 failed: {}".format(query2_error)
            logging.error(msg)
            db.close()
            bottle.abort(500, "Database error.  See the log for details.")


@bottle.route('/flipback')
def flip_one_back():
    """
    Flips a concept back to the origin language

    :param lang: (str) 3 character ISO 639-3 designation for the language
    :param target_lang: (str) 3 character ISO 639-3 designation for the target language
    :param concept_id: (str) concept identifier for the concept to be flipped
    :param user_id: (int) user id number of user making the request
    :return query2_result: (list of dicts) list converted to JSON containing the instances to be flipped back
    """
    # Validating data for the query
    if helper.is_valid_lang(bottle.request.query.target_lang):
        target_lang = bottle.request.query.target_lang
    else:
        msg = "Invalid language identifier ({}) for target language.".format(bottle.request.query.target_lang)
        logging.error(msg)
        bottle.abort(400, msg)

    if helper.is_valid_concept(bottle.request.query.concept_id):
        concept_id = bottle.request.query.concept_id
    else:
        msg = "Invalid concept identifier ({})."
        logging.error(msg)
        bottle.abort(400, msg)

    if helper.is_valid_lang(concept_id[:3]):
        lang = concept_id[:3]
    else:
        msg = "Invalid language identifier ({}) for origin language.".format(concept_id[:3])
        logging.error(msg)
        bottle.abort(400, msg)

    if helper.is_valid_uid(bottle.request.query.current_pos, "cp"):
        current_pos = bottle.request.query.current_pos
    else:
        msg = "Invalid current position identifier ({}).".format(bottle.request.query.current_pos)
        logging.error(msg)
        bottle.abort(400, msg)

    try:
        user_id = int(bottle.request.query.user_id)
    except ValueError as convert_error:
        msg = "Invalid user_id ({}): {}".format(user_id, convert_error)
        logging.error(msg)
        bottle.abort(400, msg)


    db = helper.connect_to_db(dbconf)
    cursor = db.cursor(mariadb.cursors.DictCursor)
    query1 = "DELETE FROM flipped_list WHERE user_id = {} AND concept_id = '{}'".format(user_id, concept_id)

    if helper.is_injection(query1) == False:
        try:
            cursor.execute(query1)
            db.commit()
            msg = "Query1 {} executed successfully.".format(query1)
            logging.info(msg)
        except mariadb.Error as query1_error:
            # Check for error from database indicating a duplicate entry for that user with that concept_id
            if query1_error[0] == 1062:
                logging.debug("Instance already in flipped_list for user_id {}.".format(user_id))
            else:
                db.rollback()
                msg = "Database flip query1 failed: {}".format(query1_error)
                logging.error(msg)
                bottle.abort(500, "Database error.  See the log for details.")
    else:
        msg = "Possible injection attempt: {}".format(query1)
        logging.error(msg)
        bottle.abort(400, msg)
    # TODO: fix SQL query around LIKE
    query2 = "SELECT target.instance_id AS target_instance_id, origin.instance_id AS origin_instance_id, \
              origin.instance_text AS origin_instance_text FROM {}_concept AS con INNER JOIN {} AS origin \
              ON origin.chunk_id = con.chunk_id INNER JOIN {} AS target ON origin.master_position = target.master_position \
              WHERE con.concept_id = '{}' AND origin.instance_id LIKE '{}{}' \
              ORDER BY origin.instance_id".format(lang, lang, target_lang, concept_id, current_pos, "%")

    if helper.is_injection(query2) == False:
        try:
            cursor.execute(query2)
            query2_result = cursor.fetchall()
            msg = "Query2 {} executed successfully.".format(query2)
            logging.info(msg)
            db.close()
            return json.dumps(query2_result)
        except mariadb.Error as query2_error:
            msg = "Database flip query2 failed: {}".format(query2_error)
            logging.error(msg)
            db.close()
            bottle.abort(500, "Database error.  See the log for details.")


@bottle.route('/peek')
def peek():
    """
    Retrieves information to facilitate the ability to peek at the translation of an instance before flipping it
    Parameters are retrieved from the query string of the HTTP request

    :param lang: (str) the language used for the peek
    :param mp: (str) the id of the master position for the instance the user is peeking at
    :return query_result: (list of dicts) contains the data needed to facilitate the peek functionality
    """
    # Validating/Sanitizing data for the query
    if helper.is_valid_lang(bottle.request.query.lang):
        lang = bottle.request.query.lang
    else:
        msg = "Invalid language identifier ({}) for target language.".format(bottle.request.query.target_lang)
        logging.error(msg)
        bottle.abort(400, msg)

    if helper.is_valid_uid(bottle.request.query.mp, "mp"):
        mp = bottle.request.query.mp
    else:
        msg = "Invalid master position ({}).".format(bottle.request.query.mp)
        logging.error(msg)
        bottle.abort(400, msg)

    query = "SELECT lang.instance_text FROM {} AS lang WHERE lang.master_position LIKE '{}'".format(lang, mp)
    try:
        db = helper.connect_to_db(dbconf)
        cursor = db.cursor(mariadb.cursors.DictCursor)
    except mariadb.Error as db_connect_error:
        msg = "Database connection error: {}".format(db_connect_error)
        logging.info(msg)
        bottle.abort(500, "Check the log for details.")

    if helper.is_injection(query) == False:
        try:
            cursor.execute(query)
            query_result = cursor.fetchone()
            msg = "Query {} executed successfully.".format(query)
            logging.info(msg)
            db.close()
            return json.dumps(query_result)
        except mariadb.Error as query_error:
            msg = "Database peek query ({}) failed: {}".format(query, query_error)
            logging.error(msg)
            db.close()
            bottle.abort(500, "Check the log for details.")
    else:
        logging.debug("Possible SQL injection attempt: {}.").format(query)
        db.close()


@bottle.route('/flipped')
def get_all_flipped():
    """
    Get list of all the words for the chapter that have already been flipped by the user who is logged in.
    Helper function for use in conjunction with get_chapter()
    Parameters are obtained via the query string for the API call

    :param user_id: (str) id of the user the flipped concepts are being requested for
    :param lang: (str) 3 character ISO 639-3 designation for the language
    :param target_lang: (str) 3 character ISO 639-3 designation for the target language
    :return query_result: (list of dicts) Instances to flip
    """
    # Validating/Sanitizing data for the query
    try:
        user_id = int(bottle.request.query.user_id)
    except ValueError as convert_error:
        msg = "Invalid user_id ({}): {}".format(user_id, convert_error)
        logging.error(msg)
        bottle.abort(400, msg)

    if helper.is_valid_lang(bottle.request.query.target_lang):
        target_lang = bottle.request.query.target_lang
    else:
        msg = "Invalid language identifier ({}) for target language.".format(bottle.request.query.target_lang)
        logging.error(msg)
        bottle.abort(400, msg)

    if helper.is_valid_lang(bottle.request.query.lang):
        lang = bottle.request.query.lang
    else:
        msg = "Invalid language identifier ({}) for origin language.".format(bottle.request.query.lang)
        logging.error(msg)
        bottle.abort(400, msg)

    # Query database for uids of words already flipped
    query = "SELECT origin.instance_id, target.instance_id, target.instance_text FROM user_settings AS u \
             INNER JOIN flipped_list AS f on u.user_id = f.user_id INNER JOIN {}_concept AS con ON \
             con.concept_id = f.concept_id INNER JOIN {} origin ON origin.chunk_id = con.chunk_id INNER JOIN {} \
             AS target ON origin.master_position = target.master_position WHERE u.user_id = %s \
             ORDER BY origin.instance_id".format(lang, lang, target_lang)
    
    try:
        db = helper.connect_to_db(dbconf)
        cursor = db.cursor(mariadb.cursors.DictCursor)
    except mariadb.Error as db_connect_error:
        msg = "Database connection error: {}".format(db_connect_error)
        logging.info(msg)
        bottle.abort(500, "Check the log for details.")

    if helper.is_injection(query) == False:
        try:
            cursor.execute(query, (user_id,))
            query_result = cursor.fetchall()
            msg = "Query {} executed successfully.".format(query)
            logging.info(msg)
            db.close()
            return json.dumps(query_result)
        except mariadb.Error as query_error:
            msg = "Database peek query ({}) failed: {}".format(query, query_error)
            logging.error(msg)
            db.close()
            bottle.abort(500, "Check the log for details.")
    else:
        logging.debug("Possible SQL injection attempt: {}.").format(query)
        db.close()


@bottle.route('/loaduser/<user_id>')
def load_user_data(user_id):
    """
    Loads user data on login
    :param user_id: the uid number of the user whose data were passing to the front end
    :return:
    """
    # TODO: Test function to pass user data to front end
    # Verifies that the thing being passed as the uid is actually a number or string representation of such
    try:
        user_id = int(user_id)
    except ValueError as uid_faliure:
        msg = "Invalid user_id ({}) passed in API call.".format(user_id)
        logging.error(msg)
        bottle.abort(400, "Check the log for details.")

    db = helper.connect_to_db(dbconf)
    cursor = db.cursor(mariadb.cursors.DictCursor)

    query = "SELECT * FROM user_settings WHERE user_id = %s"

    if helper.is_injection(query) == False:
        try:
            cursor.execute(query, (user_id,))
            msg = "loaduser query '{}' was executed successfully.".format(query)
            query_result = cursor.fetchone()
            logging.info(msg)
            return json.dumps(query_result)
        except mariadb.Error as query_error:
            msg = "loaduser query failed: {}".format(query_error)
            logging.error(msg)
            bottle.abort(500, "Database error.  See the log for details.")
    else:
        msg = "Possible injection attempt: {}".format(query)
        logging.error(msg)


@bottle.route('/prefs')
def save_user_preferences():
    """
    Sets the user's language preferences.  Parameters are passed in a query string.

    :param uid: (str) user id for the user whose preferences are being changed.
    :param origin_lang: (str) 3 character ISO 639-3 designation for the user's primary language.
    :param target_lang: (str) 3 character ISO 639-3 designation for the user's secondary language.
    :param rate: (int) number representing the rate at which new concepts will be flipped automatically
    :param level: (int) number representing their skill level with the target language
    :return success: (bool) Indicates a successful save of the data to the database
    """

    # TODO: Write query/code to set a user's preferences
    if helper.is_valid_lang(bottle.request.query.origin_lang):
        origin_lang = bottle.request.query.origin_lang
    else:
        msg = "Invalid language identifier ({}) for origin language.".format(bottle.request.query.origin_lang)
        logging.error(msg)
        bottle.abort(400, msg)

    if helper.is_valid_lang(bottle.request.query.target_lang):
        target_lang = bottle.request.query.target_lang
    else:
        msg = "Invalid language identifier ({}) for target language.".format(bottle.request.query.target_lang)
        logging.error(msg)
        bottle.abort(400, msg)

    try:
        uid = int(bottle.request.query.uid)
        rate = int(bottle.request.query.rate)
        level = int(bottle.request.query.level)
    except ValueError as convert_error:
        msg = "Invalid value for numeric parameter: {}".format(convert_error)
        logging.error(msg)
        bottle.abort(400, msg)
    # TODO: Add code for handling changes to user's level (adding words to list of flipped words on level increase)
    query = "UPDATE user_settings SET origin_lang_id = '{}', target_lang_id = '{}', `level` = '{}', \
             rate = '{}' WHERE user_id = %s".format(origin_lang, target_lang, level, rate)
    db = helper.connect_to_db(dbconf)
    cursor = db.cursor(mariadb.cursors.DictCursor)

    if helper.is_injection(query) == False:
        try:
            cursor.execute(query, (uid,))
            query_result = cursor.fetchone()
            db.commit()
            msg = "Query {} executed successfully.".format(query)
            logging.info(msg)
            db.close()
            return json.dumps(True)
        except mariadb.Error as query_error:
            db.rollback()
            msg = "Database preference query ({}) failed: {}".format(query, query_error)
            logging.error(msg)
            db.close()
            bottle.abort(500, "Check the log for details.")
            return json.dumps(False)
    else:
        logging.debug("Possible SQL injection attempt: {}.".format(query))
        db.close()
        bottle.abort(400, "Possible SQL injection attempt: {}.".format(query))

# TODO: Be sure to turn off debug=True!!!
if __name__ == '__main__':
    bottle.run(host='localhost', port=8000, reloader=True)
else:
    app = application = bottle.default_app()
    bottle.debug(True)
    LOGFORMAT = "%(asctime)-15s %(message)s"
    # TODO: figure out how to put log in /var/log/diglot instead of in /tmp
    logging.basicConfig(filename='/tmp/diglot.log', level=logging.DEBUG, format=LOGFORMAT)
