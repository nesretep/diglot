#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: python_api.py
# Python REST API for the Diglot Book of Mormon web app

import bottle
import json
# import instance
import helper
import sys
import pymysql as mariadb
import logging
import datetime

sys.path.extend(['/git/diglot/api'])

books = {"1Nephi": "01", "2Nephi": "02", "Jacob": "03", "Enos": "04", "Jarom": "05",
         "Omni": "06", "Words of Mormon": "7", "Mosiah": "08", "Alma": "09", "Helaman": "10",
         "3Nephi": "11", "4Nephi": "12", "Mormon": "13", "Ether": "14", "Moroni": "15"}

dbconf = "conf/diglot.conf"


@bottle.route('/')
def index(filepath="../index.html"):
    """
    Loads the page defined in the query string as "page"

    :param filename: (str) filename set by default; may be overridden
    :return content: (str) the contents of the html page specified
    :return None: return value if IOError occurs
    """
    try:
        file = open(filepath, "r")
        content = file.read()
        file.close()
        msg = "{}: File ({}) loaded successfully.".format(datetime.datetime.now(), filepath)
        logging.info(msg)
        return content
    except IOError as file_error:
        msg = "{}: Unable to open file: {}".format(datetime.datetime.now(), file_error)
        logging.error(msg)
        return None


@bottle.route('/settings')
def load_user_settings(filename="../settings.html"):
    uid = bottle.request.query.uid

    try:
        file = open(filename, "r")
        content = file.read()
        file.close()
        return content
    except IOError as file_error:
        msg = "{}: Unable to open file: {}".format(datetime.datetime.now(), file_error)
        logging.error(msg)
        return None


@bottle.route('/login')
def load_login_page(filename="../login.html"):
    try:
        file = open(filename, "r")
        content = file.read()
        file.close()
        return content
    except IOError as file_error:
        msg = "{}: Unable to open file: {}".format(datetime.datetime.now(), file_error)
        logging.error(msg)
        return None


# TODO: This will be removed before going into production and probably replaced with another function
@bottle.get('/test')
def testme():
    uid = "eng:01:01:01:001"
    try:
        table = "eng"
        db = helper.connect_to_db(dbconf)
        cursor = db.cursor(mariadb.cursors.DictCursor)
        query = "SELECT * FROM {} WHERE `instance_id` LIKE %s".format(table)
    # if helper.is_injection(query) == False:
    #     query_result = helper.run_query(cursor, query, "fetchall")
    #     return json.dumps(query_result)
    # else:
    #     index("../index.html")

        cursor.execute(query, ("eng:01:01%",))
        result = cursor.fetchall()
        cursor.close()
        msg = "{}: Query '{}' executed successfully.  Returning JSON data.".format(datetime.datetime.now(), query)
        logging.info(msg)
        return json.dumps(result)
    except mariadb.Error as error:
        # return "Exception occurred: {}".format(error)
        msg = "{}: Exception occurred: {}".format(datetime.datetime.now(), error)
        logging.error(msg)
        bottle.response.status = 500



@bottle.get('/<lang>/<book>/<chapter>')
def get_chapter(lang, book, chapter):
    """
    To return all chunks for the given chapter in JSON format

    :param lang: (str) 3 character ISO 639-3 designation for the language
    :param book: (str) the book requested in the format described by the dict 'books'
    :param chapter: (str) the chapter in the book requested
    :return: JSON-ified dict containing a list Instances for the chapter requested and a list of words flipped already
    """
    table = "eng"
    chap_uid = "{}:{}:{}{}".format(lang, books[book], chapter, "%")
    db = helper.connect_to_db(dbconf)
    cursor = db.cursor(mariadb.cursors.DictCursor)
    query = "SELECT * FROM {} t WHERE `instance_id` LIKE %s ORDER BY instance_id".format(table)
    try:
        cursor.execute(query, (chap_uid,))
        db.commit()
        query_result = cursor.fetchall()
        cursor.close()
        msg = "{}: Query {} executed successfully.  Returning JSON data.".format(datetime.datetime.now(), query)
        logging.info(msg)
        return json.dumps(query_result)
    except mariadb.Error as query_error:
        db.rollback()
        msg = "Database query failed: {}".format(query_error)
        logging.error(msg)
        bottle.response.status = 500


@bottle.put('/flip')
def flip_instance():
    """
    Sends data for switching an instance to the target langauge.  Sets one Instance as flipped in the database.
    Parameters come via a query string to form the uid being flipped.

    :param lang: (str) the language part of the uid
    :param book: (str) the book part of the uid
    :param chapter: (str) the chapter part of the uid
    :param verse: (str) the verse part of the uid
    :param pos: (str) the position in the verse part of the uid
    :param target_lang: (str)
    :param target_text: (str)
    :return query_result: JSON-ified dict containing the instance requested for the flip
    """

    lang = bottle.request.query.lang
    book = books[bottle.request.query.book]
    chapter = bottle.request.query.chapter
    verse = bottle.request.query.verse
    pos = bottle.request.query.pos
    target_lang = bottle.request.query.target_lang
    user_id = bottle.request.query.user_id

    uid = "{}:{}:{}:{}:{}".format(lang, book, chapter, verse, pos)
    if helper.is_valid_uid(uid, "instance") == False:
        msg = "Invalid uid ({}) passed to function.".format(uid)
        logging.error(msg)
        bottle.response.status = 500
        # return "<h1>HTTP 500 - Server Error</h1>"

    # Query database for chunk
    db1 = helper.connect_to_db(dbconf)
    cursor = db.cursor(mariadb.cursors.DictCursor)

    # TODO: Verify queries for flipping an instance - check variables filling the queries!
    query1 = "SELECT con.concept_id FROM {}_concept con INNER JOIN {} origin \
              WHERE origin.instance_id LIKE instance_id".format(lang, lang)
    if helper.is_injection(query1) == False:
        query1_result = helper.run_query(cursor, query1, "fetchone")
    else:
        index("../index.html")

    query2 = "INSERT INTO flipped_list (user_id, concept_id) VALUES ({}, {})".format(user_id,
                                                                                     query1_result['concept_id'])
    if helper.is_injection(query2) == False:
        query2_result = helper.run_query(cursor, query2, "insert")
    else:
        index("../index.html")

    query3 = "SELECT origin.master_position FROM {} origin WHERE origin.instance_id LIKE '{}'".format(target_lang, uid)
    if helper.is_injection(query3) == False:
        query3_result = helper.run_query(cursor, query2, "fetchone")
    else:
        index("../index.html")

    query4 = "SELECT target.instance_id, target.instance_text FROM {} target \
              WHERE target.instance_id LIKE '{}'".format(target_table, query3_result['instance_id'])
    if helper.is_injection(query4) == False:
        query4_result = helper.run_query(cursor, query2, "fetchone")
    else:
        index("../index.html")

    return json.dumps(query4_result)
    # try:
    #     cursor.execute(query1)
    #     db.commit()
    #     query_result = cursor.fetchone()
    #     msg = "{}: Query {} executed successfully.  Returning JSON data.".format(datetime.datetime.now(), query)
    #     logging.info(msg)
    #     return json.dumps(query_result)
    # except mariadb.Error as query_error:
    #     db.rollback()
    #     msg = "Database query failed: {}".format(query_error)
    #     logging.error(msg)
    #     return "Database query failed: {}".format(query_error)


@bottle.route('/flipped')
def get_all_flipped():
    """
    Get list of all the words for the chapter that have already been flipped.
    Helper function for use in get_chapter()

    :return query_result: (list of dicts) Instances to flip
    """
    # Query database for uids of words already flipped
    try:
        db = helper.connect_to_db(dbconf)
        cursor = db.cursor(mariadb.cursors.DictCursor)
    except Exception as db_connect_error:
        return "Database connection error: {}".format(db_connect_error)

    query = "SELECT * FROM user_lm WHERE userid = ? AND flipped = True"

    try:
        cursor.execute(query, (userid,))
        db.commit()
        query_result = cursor.fetch_all()
    except mariadb.Error as query_error:
        db.rollback()
        return "Database query failed: {}".format(query_error)
    finally:
        cursor.close()
        db.close()

    return query_result


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


@bottle.put('/prefs/<uid>')
def set_user_prefs(uid):
    """
    Sets the user's level in their user preferences.
    Some parameters are obtained from the query string (marked with a * below).

    *:param level: (int) Indicates the difficulty the user is comfortable with
    *:param target: (str) ISO 639-3 identifier for the target language chosen

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
        bottle.response.status = 500
        return "Database query failed: {}".format(query_error)
    finally:
        cursor.close()
        db.close()

    return confirm_level_set


# TODO: Verify whether or not this URL format will work the way we intend it to
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


# TODO: Be sure to turn off debug before this goes into production
if __name__ == '__main__':
    bottle.run(host='localhost', port=8000, debug=True, reloader=True)
else:
    app = application = bottle.default_app()
    bottle.debug(True)
    logging.basicConfig(filename='/tmp/test.log', level=logging.DEBUG)
