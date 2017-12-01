#!usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: python_api.py
# trying out writing a basic API

import bottle
import json
import chunk
import helper
import sqlalchemy

books = {"1Nephi": "01", "2Nephi": "02", "Jacob": "03", "Enos": "04", "Jarom": "05",
         "Omni": "06", "Words of Mormon": "7", "Mosiah": "08", "Alma": "09", "Helaman": "10",
         "3Nephi": "11", "4Nephi": "12", "Mormon": "13", "Ether": "14", "Moroni": "15"}

# TODO: This will be removed before going into production
@bottle.route('/')
def testme():
    engine = helper.connect_to_db("sqlalchemy", "conf/diglot.conf")
    metadata = sqlalchemy.MetaData(engine)
    table = sqlalchemy.Table("ENG", metadata, autoload=True)
    query = table.select()
    connection = engine.connect()
    trans = connection.begin()
    try:
        query_result = connection.execute(query)
        trans.commit()
    except BaseException:
        trans.rollback()
        raise
    for item in query_result:
        print item



# TODO: Check all route decorators with Daniel to make sure they make sense
@bottle.route('/login')
def do_login():
    """
    Gets the username and password that was sent in the form ans performs authentication

    :return: (bool) Value indicating login status
    """
    username = bottle.request.forms.get('username')
    password = bottle.request.forms.get('password')
    return json.dumps(helper.check_login(username, password))
    # return json.dumps(chunk.Chunk("ENG:01:01:01:001", "my text", "01:01:01:001", 7).to_dict())

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

    :param lang: (str) 2 character ISO 639-1 designation for the language
    :param book: (str) the book requested
    :param chapter: (str) the chapter in the book requested
    :return chapter_chunks: list of Chunks for the chapter requested
    """
    # TODO: Should this also return the corresponding info for the secondary language?

    chap_uid = "{}:{}:{}".format(lang, books[book], chapter)
    chapter_list = []  # list to hold Chunk objects

    # Query prep work
    engine = helper.connect_to_db("sqlalchemy", "conf/diglot.conf")
    metadata = sqlalchemy.MetaData(engine)
    table1 = sqlalchemy.Table(lang, metadata, autoload=True)
    # table2 = sqlalchemy.Table("user_lm", metadata, autoload=True)
    # TODO: Check the syntax of the substr function call; finish join query
    # join1 = sqlalchemy.join(table1, table2, )
    query1 = table1.select(sqlalchemy.func.substr(table.c.uid, 1, 8) == chap_uid)


    # Connect to database and perform the query
    connection = engine.connect()
    trans = connection.begin()
    try:
        query_result = connection.execute(query1)
        trans.commit()
    except BaseException:
        trans.rollback()
        raise

    # Create a Chunk object for each chunk in query results, append Chunk to list
    for item in query_result:
        # TODO: Verify what 'item' contains to make sure it is in the proper format for making a Chunk like this
        chapter_list.append(chunk.Chunk(item['uid'], item['text'], item['masterpos'], item['rank'],
                                        item['flipped'], item['tag'], item['suggested']))
    # sort chapter_list and then convert it to JSON format
    chapter_list = sorted(chapter_list)
    flipped_words = sorted(helper.get_flipped_words())
    # Close database connection
    connection.close()

    # return JSON-ified version of chapter_list and flipped words in a json of jsons
    return json.dumps({"chapter": chapter_list, "flipped": flipped_words})


@bottle.route('/chunk/<uid>')
def get_one_chunk(uid):
    """
    Get one Chunk from the database and return it to the function caller.

    :param uid: (str) the uid for the Chunk requested.
    :return: (Chunk) The Chunk with the uid specified in the function call in JSON format.
    :return None: returns None if uid is not valid
    """
    if helper.is_valid_uid(uid, "chunk"):
        # Query database for chunk
        engine = helper.connect_to_db('sqlalchemy', 'conf/diglot.conf')
        metadata = sqlalchemy.MetaData(engine)
        connection = engine.connect()
        trans = connection.begin()
        lang = uid.split(":")[0]
        table = sqlalchemy.Table(lang, metadata, autoload=True)
        query = table.select(table.c.uid == uid)

        try:
            query_result = connection.execute(query)
            trans.commit()
        except BaseException:
            trans.rollback()
            raise
        # Create Chunk object
        # TODO: Fix creation of chunk object.  Not all data will be provided by current query!
        mychunk = chunk.Chunk(query_result['uid'], query_result['text'], query_result['masterpos'],
                              query_result['rank'], query_result['flipped'], query_result['tag'],
                              query_result['suggested'])
        connection.close()

        return json.dumps(mychunk.to_dict())
    else:
        return None


@bottle.put('/flip/<uid>')
def flip_one_chunk(uid):
    """
    Sets one Chunk as flipped in the database.

    :param uid: (str) The Chunk uid that needs to be set as flipped.
    :return confirm_flip: (tuple) (boolean, str/None)
            True to confirm it was flipped, False to indicate an error
            Error message if there was an error, None if invalid uid
    """
    if helper.is_valid_uid(uid, "chunk"):
        # Update record for chunk with matching uid to set
        engine = helper.connect_to_db('sqlalchemy', 'conf/diglot.conf')
        metadata = sqlalchemy.MetaData(engine)
        connection = engine.connect()
        trans = connection.begin()

        # TODO: Write this query for flipping one chunk
        query = ""

        try:
            query_result = connection.execute(query)
            trans.commit()
            confirm_flip = True
        except Exception:
            trans.rollback()
            confirm_flip = False
            raise
        connection.close()
        return confirm_flip
    else:
        return None


# @bottle.put('/update')
# def set_flipped_list(chunks):
#     """
#     Updates the database with Chunks that were flipped in that session
#
#     :param chunks: (list) Chunks to be set as flipped in the database
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
    engine = helper.connect_to_db('sqlalchemy', 'conf/diglot.conf')
    metadata = sqlalchemy.MetaData(engine)
    connection = engine.connect()
    trans = connection.begin()
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
    engine = helper.connect_to_db('sqlalchemy', 'conf/diglot.conf')
    metadata = sqlalchemy.MetaData(engine)
    connection = engine.connect()
    trans = connection.begin()
    # TODO: Write query to set user's level
    query = ""

    try:
        query_result = connection.execute(query)
        trans.commit()
        confirm_level_set = True
    except Exception:
        trans.rollback()
        confirm_level_set = False
        raise
    connection.close()
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
        engine = helper.connect_to_db('sqlalchemy', 'conf/diglot.conf')
        metadata = sqlalchemy.MetaData(engine)
        connection = engine.connect()
        trans = connection.begin()
        # TODO: Write query to set a user's primary and secondary language
        query = ""

        try:
            query_result = connection.execute(query)
            trans.commit()
            confirm_lang_set = True
        except Exception:
            trans.rollback()
            confirm_lang_set = False
            raise
        connection.close()
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
    engine = helper.connect_to_db('sqlalchemy', 'conf/diglot.conf')
    metadata = sqlalchemy.MetaData(engine)
    connection = engine.connect()
    trans = connection.begin()
    table = sqlalchemy.Table(lang, metadata, autoload=True)
    # TODO: Write query to get the next (3?) suggested chunks from the database based on the chapter they are in
    query = table.select(sqlalchemy.and_(sqlalchemy.func.substr(table.c.uid, 1, 8), table.c.rank == level,
                         table.c.suggested == False))

    try:
        query_result = connection.execute(query)
        trans.commit()
        confirm_lang_set = True
    except Exception:
        trans.rollback()
        confirm_lang_set = False
        raise

    connection.close()
    return json.dumps(query_result)


# TODO: Be sure to turn off debug before this goes into production
if __name__ == '__main__':
    bottle.run(host='192.168.80.0', port=8000, debug=True, reloader=True)
else:
    app = application = bottle.default_app()
