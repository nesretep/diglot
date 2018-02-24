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
# TODO: remove return statements that reveal debugging info from all functions


@bottle.route('/')
def index(filepath="../index.html"):
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


@bottle.route('/settings')
def load_user_settings(filename="../settings.html"):
    """
    Loads the settings page.

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


# TODO: This will be removed before going into production and probably replaced with another function
@bottle.get('/test')
def testme():
    uid = "eng:01:01:01:001"
    try:
        target_lang = "spa"
        concept_id = "eng_con_00001"
        db = helper.connect_to_db(dbconf)
        cursor = db.cursor(mariadb.cursors.DictCursor)
        lang = "eng"
        mp = "01:01:01:001"
        # query = "SELECT * FROM {} WHERE `instance_id` LIKE %s".format(table)
        query = "SELECT origin.instance_id, target.instance_id, target.instance_text FROM {}_concept AS con \
                  INNER JOIN {} AS origin ON origin.chunk_id = con.chunk_id INNER JOIN {} AS target ON origin.master_position = target.master_position \
                  WHERE con.concept_id = {} \
                  ORDER BY origin.instance_id".format(lang, lang, target_lang, concept_id)
        if helper.is_injection(query) == False:
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            msg = "Test query '{}' executed successfully.".format(query)
            logging.info(msg)
            return json.dumps(result)
    except mariadb.Error as error:
        # return "Exception occurred: {}".format(error)
        msg = "Exception occurred: {}".format(error)
        logging.error(msg)
        bottle.abort(500, "Test failed: {}".format(msg))


@bottle.get('/<lang>/<book>/<chapter>')
def get_chapter(lang, book, chapter):
    """
    To return all chunks for the given chapter in JSON format

    :param lang: (str) 3 character ISO 639-3 designation for the language
    :param book: (str) the book requested in the format described by the dict 'books'
    :param chapter: (str) the chapter in the book requested
    :return: JSON-ified dict containing a list Instances for the chapter requested and a list of words flipped already
    """
    chap_uid = "{}:{}:{}{}".format(lang, books[book], chapter, "%")
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


@bottle.route('/flip')
def flip_one_concept():
    """
    Sends data for switching an instance to the target language.  Sets one Instance as flipped in the database.
    Parameters are retrieved from the query string of the HTTP request

    :param concept_id: (str) concept identifier for the concept to be flipped
    :param user_id: (str) id of the user for which the concept is being flipped
    :param target_lang: (str) 3 character ISO 639-3 designation for the target language
    :return query2_result: JSON-ified dict containing the instance requested for the flip
    """
    target_lang = bottle.request.query.target_lang
    user_id = int(bottle.request.query.user_id)
    concept_id = bottle.request.query.concept_id
    lang = concept_id[:3]

    # Query database for chunk
    db = helper.connect_to_db(dbconf)
    cursor = db.cursor(mariadb.cursors.DictCursor)

    # either adds or removes the concept selected from the table depending on whether the user is flipping the
    # concept to the target language or back to the origin language from the target language
    query1 = "INSERT INTO flipped_list (user_id, concept_id) VALUES ('{}', '{}')".format(user_id, concept_id)
    if helper.is_injection(query1) == False:
        try:
            cursor.execute(query1)
            db.commit()
            query1_result = cursor.fetchone()  # TODO: Do we need this line?
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
    query2 = "SELECT origin.instance_id AS origin_instance_id, target.instance_id AS target_instance_id, \
              target.instance_text AS target_instance_text FROM {}_concept AS con INNER JOIN {} AS origin ON \
              origin.chunk_id = con.chunk_id INNER JOIN {} AS target ON origin.master_position = target.master_position \
              WHERE con.concept_id = '{}' ORDER BY origin.instance_id".format(lang, lang, target_lang, concept_id)
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
    target_lang = bottle.request.query.target_lang
    user_id = int(bottle.request.query.user_id)
    concept_id = bottle.request.query.concept_id
    lang = concept_id[:3]

    db = helper.connect_to_db(dbconf)
    cursor = db.cursor(mariadb.cursors.DictCursor)
    query1 = "DELETE FROM flipped_list WHERE user_id = {} AND concept_id = '{}'".format(user_id, concept_id)

    if helper.is_injection(query1) == False:
        try:
            cursor.execute(query1)
            db.commit()
            query1_result = cursor.fetchone()  # TODO: Do we need this line?
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

    query2 = "SELECT target.instance_id AS target_instance_id, origin.instance_id AS origin_instance_id, \
              origin.instance_text AS origin_instance_text FROM {}_concept AS con INNER JOIN {} AS origin \
              ON origin.chunk_id = con.chunk_id INNER JOIN {} AS target ON origin.master_position = target.master_position \
              WHERE con.concept_id = '{}' ORDER BY origin.instance_id".format(lang, lang, target_lang, concept_id)

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
    lang = bottle.request.query.lang
    mp = bottle.request.query.mp

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

    :param user_id: (str) id of the user the flipped concepts are being requested for
    :return query_result: (list of dicts) Instances to flip
    """
    user_id = bottle.request.query.user_id
    lang = bottle.request.query.lang
    target_lang = bottle.request.query.target_lang

    # Query database for uids of words already flipped
    query = "SELECT origin.instance_id, target.instance_id, target.instance_text FROM user_settings AS u \
             INNER JOIN flipped_list AS f on u.user_id = f.user_id INNER JOIN {}_concept AS con ON \
             con.concept_id = f.concept_id INNER JOIN {} origin ON origin.chunk_id = con.chunk_id INNER JOIN {} \
             AS target ON origin.master_position = target.master_position WHERE user_id = user_id \
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


# @bottle.route('')
def past_critical_point():
    """
    Checks if user is past critical point

    :return critical: (boolean) True if past critical point, False if not
    """

    query = ""
    """
        Something goes here...
    """
    critical = False
    return critical


@bottle.put('/setlevel')
def set_user_level():
    """
    Sets the user's level in their user preferences.
    Parameters are obtained from the query string

    :param level: (int) Indicates the difficulty the user is comfortable with
    :param target: (str) ISO 639-3 identifier for the target language chosen

    :param uid: (str) The id of the user

    :return confirm_level_set: (tuple) (boolean, str/None)
            True to indicate update was successful, False if error
            Error message if there was an error, None if invalid uid
    """
    # get values from URL query string
    uid = bottle.request.query.uid
    level = int(bottle.request.query.level)

    try:
        db = helper.connect_to_db(dbconf)
        cursor = db.cursor(mariadb.cursors.DictCursor)
    except Exception as db_connect_error:
        return "Database connection error: {}".format(db_connect_error)

    query = "UPDATE user_lm SET level=%d WHERE user_id=%s"

    try:
        cursor.execute(query, (level, uid))
        db.commit()
        query_result = cursor.fetchone()
    except mariadb.Error as query_error:
        db.rollback()
        bottle.abort(500, "Test")
        return "Database query failed: {}".format(query_error)
    finally:
        cursor.close()
        db.close()

    return confirm_level_set


@bottle.route('/prefs')
def set_user_language():
    """
    Sets the user's language preferences.  Parameters are passed in a query string.

    :param uid: (str) user id for the user whose preferences are being changed.
    :param p_lang: (str) 3 character ISO 639-2 designation for the user's primary language.
    :param s_lang: (str) 3 character ISO 639-2 designation for the user's secondary language.
    :return confirm_lang_set: (tuple) (boolean, str/None)
            True to indicate update was successful, False if error
            Error message if there was an error, None if invalid uid
    """
    # TODO: Write query to set a user's primary and secondary language
    query = ""

    try:

        confirm_lang_set = True
    except Exception:

        confirm_lang_set = False
        raise

    return confirm_lang_set


@bottle.get('/<lang>/<level>/suggest')
def get_suggestions(lang, level):
    """
    Grabs a set of suggested words for the given language and level

    :param lang: (str) 2 character ISO 639-1 designation for the language
    :param level: (int) the user's level of comfort with the language
    :return: JSON of suggested words from database
    """

    # TODO: Write query/code to get the next batch of suggested chunks
    # from the database based on the chapter they are in
    query = ""


# TODO: Be sure to turn off debug=True!!!
if __name__ == '__main__':
    bottle.run(host='localhost', port=8000, reloader=True)
else:
    app = application = bottle.default_app()
    bottle.debug(True)
    LOGFORMAT = "%(asctime)-15s %(message)s"  # TODO: implement proper log formatting (optional)
    # TODO: figure out how to put log in /var/log and have it work properly
    logging.basicConfig(filename='/tmp/diglot.log', level=logging.DEBUG, format=LOGFORMAT)
