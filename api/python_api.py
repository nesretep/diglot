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


@bottle.route('/<lang>/<book>/<chapter>')
def get_chapter(lang, book, chapter):
    """
    To return all chunks for the given chapter in JSON format

    :param book: (str) the book requested
    :param chapter: (str) the chapter in the book requested
    :return chapter_chunks: list of Chunks for the chapter requested
    """
    # TODO: Should this also return the corresponding info for the secondary language?

    chap_uid = "{}:{}:{}:{}:{}".format(lang, books[book], chapter, "00", "00")
    chapter_list = []
    # Connect to database
    engine = helper.connect_to_db("sqlalchemy", "conf/diglot.conf")

    # Construct query: use SQL Alchemy functions to do it if possible
    query = ""

    # Execute Query to database to retrieve all chunks for the given book and chapter
    connection = engine.connect()
    trans = connection.begin()
    try:
        query_result = connection.execute(query)
        trans.commit()
    except:
        trans.rollback()
        raise

    # Create a Chunk object for each, append Chunk to chapter_list
    for item in query_result:
        # TODO: Verify what 'item' contains to make sure it is in the proper format for making a Chunk like this
        chapter_list.append(chunk.Chunk(item['uid'], item['text'], item['masterpos'], item['rank'],
                                        item['flipped'], item['tag'], item['suggested']))
    # sort chapter_list and then convert it to JSON format
    chapter_list = sorted(chapter_list)
    # Close database connection
    connection.close()
    # return JSON-ified version of chapter_list
    return json.dumps(chapter_list)


# No route since it is a helper function
def get_flipped_words():
    """
    Get list of all the words for the chapter that have already been flipped.
    Helper function for use in get_chapter()

    :return words: (list) Chunk uids to flip
    """
    # Query database for uids of words already flipped
    return json.dumps(query_results)


@bottle.route('/chunk/<uid>')
def get_one_chunk(uid):
    """
    Get one Chunk from the database and return it to the function caller.

    :param uid: (str) the uid for the Chunk requested.
    :return chunk: (Chunk) The Chunk with the uid specified in the function call.
    """
    # Query database for chunk
    # Create Chunk object
    return json.dumps(chunk.__dict__)


@bottle.route('/flip/<uid>')
def flip_one_chunk(uid):
    """
    Sets one Chunk as flipped in the database.

    :param uid: (str) The Chunk uid that needs to be set as flipped.
    :return confirm_flip: (tuple) (boolean, str/None)
            True to confirm it was flipped, False to indicate an error
            Error message if there was an error, None if no error
    """
    # Update record for chunk with matching uid to set
    return confirm_flip


@bottle.route('/update')
def set_flipped_list(chunks):
    """
    Updates the database with Chunks that were flipped in that session

    :param chunks: (list) Chunks to be set as flipped in the database
    :return confirm_list_set: (tuple) (boolean, str/None)
            True to indicate update was successful, False if error
            Error message if there was an error, None if no error
    """
    pass


# @bottle.route('')
def past_critical_point():
    """
    Checks if user is past critical point

    :return critical: (boolean) True if past critical point, False if not
    """
    pass


@bottle.route('/prefs/<uid>/<level>')
def set_user_level(uid, level):
    """
    Sets the user's level in their user preferences.

    :param level: (int) Indicates the difficulty the user is comfortable with
    :return confirm_level_set: (tuple) (boolean, str/None)
            True to indicate update was successful, False if error
            Error message if there was an error, None if no error
    """
    # run update query to database for given uid to set level to level given.
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
            Error message if there was an error, None if no error
    """
    pass
