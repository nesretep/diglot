#!usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: python_api.py
# Python REST API for the Diglot Book of Mormon web app

import bottle
import json
import instance
import helper
import sys
import pymysql as mariadb
import logging
import datetime

sys.path.extend(['/git/diglot/api'])

#TODO: Should we implement logging?

books = {"1Nephi": "01", "2Nephi": "02", "Jacob": "03", "Enos": "04", "Jarom": "05",
         "Omni": "06", "Words of Mormon": "7", "Mosiah": "08", "Alma": "09", "Helaman": "10",
         "3Nephi": "11", "4Nephi": "12", "Mormon": "13", "Ether": "14", "Moroni": "15"}

dbconf = "conf/diglot.conf"


@bottle.route('/')
def start(filepath="../index.html"):
    """
    Loads the page defined in the query string as "page"

    :param filename: (str) filename set by default; may be overridden
    :return content: (str) the contents of the html page specified
    :return None: return value if IOError occurs
    """
    # if bottle.request.query.page is not None:
    #     filename = "{}{}{}".format("../", bottle.request.query.page, ".html")
    # else:
    #     pass

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
def load_settings(filename="../settings.html"):
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
def load_login(filename="../login.html"):
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
        db = helper.connect_to_db(dbconf)
        cursor = db.cursor(mariadb.cursors.DictCursor)
        query = "SELECT * FROM eng_test"
        # query = "SHOW tables"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return json.dumps(result)
    except Exception as error:
        return "Exception occurred: {}".format(error)

# TODO: flesh out this function!
@bottle.route('/header')
def get_chapter_header(request):
    """
    Gets chapter heading text from the database and returns it

    :param request: the chapter you are requesting the header for
    :return: ????
    """
    db = helper.connect_to_db(dbconf)
    cursor = db.cursor(mariadb.cursors.DictCursor)
    # TODO: write query for retrieving the chapter header text
    query = "Select the stuff from the place when it looks right."

    try:
        cursor.execute(query)
        db.commit()
        query_result = cursor.fetchone()
        cursor.close()
        msg = "{}: Query {} executed successfully.".format(datetime.datetime.now(), query)
        logging.info(msg)
        return json.dumps(query_result)
    except mariadb.Error as query_error:
        db.rollback()
        msg = "Database query failed: {}".format(query_error)
        logging.error(msg)
        return msg


@bottle.get('/<lang>/<book>/<chapter>')
def get_chapter(lang, book, chapter):
    """
    To return all chunks for the given chapter in JSON format

    :param lang: (str) 3 character ISO 639-3 designation for the language
    :param book: (str) the book requested in the format described by the dict 'books'
    :param chapter: (str) the chapter in the book requested
    :return: JSON-ified dict containing a list Instances for the chapter requested and a list of words flipped already
    """
    table = "eng_test"
    chap_uid = "{}:{}:{}{}".format(lang, books[book], chapter, "%")
    db = helper.connect_to_db(dbconf)
    cursor = db.cursor(mariadb.cursors.DictCursor)
    query = "SELECT * FROM {} WHERE `natural_position` LIKE %s".format(table)

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
        return msg


@bottle.route('/instance')
def get_one_instance():
    """
    Get one Instance from the database and return it to the function caller.

    :param uid: (str) the uid for the Instance requested.
    :return: (Instance) The Instance with the uid specified in the function call in JSON format.
    :return None: returns None if uid is not valid
    """
    lang = bottle.request.query.lang
    book = books[bottle.request.query.book]
    chapter = bottle.request.query.chapter
    verse = bottle.request.query.verse
    pos = bottle.request.query.pos

    uid = "{}:{}:{}:{}:{}".format(lang, book, chapter, verse, pos)

    if helper.is_valid_uid(uid, "instance") is True:
        # Query database for chunk
        try:
            db = helper.connect_to_db(dbconf)
            cursor = db.cursor(mariadb.cursors.DictCursor)
        except Exception as db_connect_error:
            return "Database connection error: {}".format(db_connect_error)

        # table = uid[:3]
        table = "eng_test"
        query = "SELECT * FROM {} WHERE natural_position=%s".format(table)

        try:
            cursor.execute(query, (uid,))
            db.commit()
            query_result = cursor.fetchone()
            msg = "{}: Query {} executed successfully.  Returning JSON data.".format(datetime.datetime.now(), query)
            logging.info(msg)
            return json.dumps(query_result)
        except mariadb.Error as query_error:
            db.rollback()
            msg = "Database query failed: {}".format(query_error)
            logging.error()
            return "Database query failed: {}".format(query_error)


@bottle.put('/flip')
def flip_instance():
    """
    Sets one Instance as flipped in the database.

    :param uid: (str) The Instance uid that needs to be set as flipped.
    :return confirm_flip: (tuple) (boolean, str/None)
            True to confirm it was flipped, False to indicate an error
            Error message if there was an error, None if invalid uid
    """
    if helper.is_valid_uid(uid, "instance") is True:
        # Query database for chunk
        try:
            db = helper.connect_to_db(dbconf)
            cursor = db.cursor(mariadb.cursors.DictCursor)
        except Exception as db_connect_error:
            return "Database connection error: {}".format(db_connect_error)

        # table = uid[:3]
        table = "eng_test"
        query = "SELECT * FROM {} WHERE natural_position=%s".format(table)

        try:
            cursor.execute(query, (uid,))
            db.commit()
            query_result = cursor.fetchone()
            msg = "{}: Query {} executed successfully.  Returning JSON data.".format(datetime.datetime.now(), query)
            logging.info(msg)
            return json.dumps(query_result)
        except mariadb.Error as query_error:
            db.rollback()
            msg = "Database query failed: {}".format(query_error)
            logging.error()
            return "Database query failed: {}".format(query_error)


def get_flipped():
    """
    Get list of all the words for the chapter that have already been flipped.
    Helper function for use in get_chapter()

    :return words: (list) Instance uids to flip
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
        # TODO: Check format of query result to make sure it is OK for coverting to JSON!
        query_result = cursor.fetch_all()
    except mariadb.Error as query_error:
        db.rollback()
        return "Database query failed: {}".format(query_error)
    finally:
        cursor.close()
        db.close()

    return query_result


# @bottle.put('/update')
# def set_flipped_list(chunks):
#     """
#     Updates the database with Instances that were flipped in that session
#
#     :param chunks: (list) Instances to be set as flipped in the database
#     :return confirm_list_set: (tuple) (boolean, str/None)
#             True to indicate update was successful, False if error
#             Error message if there was an error, None if invalid uid
#     """
#     engine = helper.connect_to_db('sqlalchemy', 'conf/diglot.conf')
#     metadata = sqlalchemy.MetaData(engine)
#     connection = engine.connect()
#     trans = connection.begin()
#     chunks = json.loads(chunks)
#     # TODO: Figure out how to best structure this data and then process it.
#     for uid in chunks:
#
#     query = ""
#
#     try:
#         query_result = connection.execute(query)
#         trans.commit()
#         confirm_list_set = True
#     except Exception:
#         trans.rollback()
#         confirm_list_set = False
#         raise
#     connection.close()
#     return confirm_list_set


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


@bottle.put('/prefs/<uid>/<level>')
def set_user_level(uid, level):
    """
    Sets the user's level in their user preferences.

    :param level: (int) Indicates the difficulty the user is comfortable with
    :return confirm_level_set: (tuple) (boolean, str/None)
            True to indicate update was successful, False if error
            Error message if there was an error, None if invalid uid
    """
    # run update query to database for given uid to set level to level given.

    # TODO: Write query to set user's level
    query = ""


    return confirm_level_set


# TODO: Verify whether or not this URL format will work the way we intend it to
@bottle.route('/prefs/<uid>/<p_lang>-<s_lang>')
def set_user_language(uid, p_lang, s_lang):
    """
    Sets the user's language preferences.

    :param p_lang: (str) 2 character ISO 639-1 designation for the user's primary language.
    :param s_lang: (str) 2 character ISO 639-1 designation for the user's secondary language.
    :return confirm_lang_set: (tuple) (boolean, str/None)
            True to indicate update was successful, False if error
            Error message if there was an error, None if invalid uid
    """
    if helper.is_valid_uid(uid, "chunk"):
        # TODO: Write query to set a user's primary and secondary language
        query = ""

        try:

            confirm_lang_set = True
        except Exception:

            confirm_lang_set = False
            raise

        return confirm_lang_set
    else:
        return None


@bottle.get('/<lang>/<level>/suggest')
def get_suggestions(lang, level):
    """
    Grabs a set of suggested words for the given language and level

    :param lang: (str) 2 character ISO 639-1 designation for the language
    :param level: (int) the user's level of comfort with the language
    :return: JSON of suggested words from database
    """

    # TODO: Write query to get the next (3?) suggested chunks from the database based on the chapter they are in
    query = ""

    try:

        confirm_lang_set = True
    except Exception:

        confirm_lang_set = False
        raise
    return json.dumps(query_result)


# TODO: Be sure to turn off debug before this goes into production
if __name__ == '__main__':
    bottle.run(host='localhost', port=8000, debug=True, reloader=True)
else:
    app = application = bottle.default_app()
    bottle.debug(True)
    logging.basicConfig(filename='/tmp/test.log', level=logging.DEBUG)
