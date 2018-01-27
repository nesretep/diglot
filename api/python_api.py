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

sys.path.extend(['/git/diglot/api'])

#TODO: Should we implement logging?

books = {"1Nephi": "01", "2Nephi": "02", "Jacob": "03", "Enos": "04", "Jarom": "05",
         "Omni": "06", "Words of Mormon": "7", "Mosiah": "08", "Alma": "09", "Helaman": "10",
         "3Nephi": "11", "4Nephi": "12", "Mormon": "13", "Ether": "14", "Moroni": "15"}

dbconf = "conf/diglot.conf"


# TODO: This will be removed before going into production and probably replaced with another function
@bottle.get('/')
def testme():
    uid = "eng:01:01:01:001"
    try:
        db = helper.connect_to_db(dbconf, adminuser=True)
        cursor = db.cursor()
        query = "SELECT * FROM eng_test"
        # query = "SHOW tables"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return json.dumps(result)
    except Exception as error:
        return "Exception occurred: {}".format(error)


@bottle.route('/login')
def do_login():
    """
    Gets the username and password that was sent in the form ans performs authentication

    :return: (bool) Value indicating login status
    """
    username = bottle.request.forms.get('username')
    password = bottle.request.forms.get('password')
    return json.dumps(helper.check_login(username, password))
    # return json.dumps(chunk.Instance("ENG:01:01:01:001", "my text", "01:01:01:001", 7).to_dict())


@bottle.get('/static/<filename>')
def get_static(filename):
    """
    This function facilitates the retrieval of static files as needed.

    :param filename: name of static file requested
    :return: the file that was requested
    """
    static_webroot = "/var/www/html/static/"
    return bottle.static_file(filename, root=static_webroot)


@bottle.get('/<lang>/<book>/<chapter>')
def get_chapter(lang, book, chapter):
    """
    To return all chunks for the given chapter in JSON format

    :param lang: (str) 3 character ISO 639-3 designation for the language
    :param book: (str) the book requested in the format described by the dict 'books'
    :param chapter: (str) the chapter in the book requested
    :return: JSON-ified dict containing a list Instances for the chapter requested and a list of words flipped already
    """
    chap_uid = "{}:{}:{}".format(lang, books[book], chapter)
    chapter_list = []  # list to hold Instance objects

    # Query prep work
    try:
        db = helper.connect_to_db(dbconf)
        cursor = db.cursor()
    except Exception as db_connect_error:
        return "Database connection error: {}".format(db_connect_error)
    #TODO: Do we need a semicolon at the end of queries or not?
    query = "SELECT * FROM ? WHERE uid LIKE ?"

    try:
        cursor.execute(query, (lang, chap_uid + "%"))
        db.commit()
        query_result = cursor.fetch_all()
    except mariadb.Error as query_error:
        db.rollback()
        return "Database query failed: {}".format(query_error)
    finally:
        cursor.close()
        db.close()

    # Create a Instance object for each instance in query results, append Instance to list
    for item in query_result:
        # TODO: Verify what 'item' contains to make sure it is in the proper format for making an Instance like this!
        chapter_list.append(instance.Instance(item['uid'], item['text'], item['masterpos'], item['rank'], item['flipped'],
                                        item['tag'], item['suggested']))
    # sort chapter_list and then convert it to JSON format
    chapter_list = sorted(chapter_list)
    # TODO: implement this function to get the already flipped words
    flipped_words = sorted(get_flipped_words())

    # return JSON-ified version of chapter_list and flipped words in a json of jsons
    return json.dumps({"chapter": chapter_list, "flipped": flipped_words})


@bottle.route('/chunk/<uid>')
def get_one_chunk(uid):
    """
    Get one Instance from the database and return it to the function caller.

    :param uid: (str) the uid for the Instance requested.
    :return: (Instance) The Instance with the uid specified in the function call in JSON format.
    :return None: returns None if uid is not valid
    """
    if helper.is_valid_uid(uid, "instance"):
        # Query database for chunk
        try:
            db = helper.connect_to_db(dbconf)
            cursor = db.cursor()
        except Exception as db_connect_error:
            return "Database connection error: {}".format(db_connect_error)

        table = uid[:3]
        query = "SELECT * FROM ? WHERE uid = ?"

        try:
            cursor.execute(query, (table, uid))
            db.commit()
            query_result = cursor.fetch_all()
        except mariadb.Error as query_error:
            db.rollback()
            return "Database query failed: {}".format(query_error)
        finally:
            cursor.close()
            db.close()
        # Create Instance object
        # TODO: Fix creation of chunk object.  Not all data will be provided by current query!
        mychunk = instance.Instance(query_result['uid'], query_result['text'], query_result['masterpos'],
                               query_result['rank'], query_result['flipped'], query_result['tag'],
                               query_result['suggested'])

        return json.dumps(mychunk.to_dict())
    else:
        return None


@bottle.put('/flip/<uid>')
def flip_one_chunk(uid):
    """
    Sets one Instance as flipped in the database.

    :param uid: (str) The Instance uid that needs to be set as flipped.
    :return confirm_flip: (tuple) (boolean, str/None)
            True to confirm it was flipped, False to indicate an error
            Error message if there was an error, None if invalid uid
    """
    if helper.is_valid_uid(uid, "chunk"):
        # Update record for chunk with matching uid to set
        try:
            db = helper.connect_to_db(dbconf)
            cursor = db.cursor()
        # TODO: Write this query for flipping one chunk
        except Exception as error:
            raise

        try:

            confirm_flip = True
        except Exception:
            confirm_flip = False
            raise
        cursor.close()
        return confirm_flip
    else:
        return None


def get_flipped_words():
    """
    Get list of all the words for the chapter that have already been flipped.
    Helper function for use in get_chapter()

    :return words: (list) Instance uids to flip
    """
    # Query database for uids of words already flipped
    try:
        db = helper.connect_to_db(dbconf)
        cursor = db.cursor()
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
