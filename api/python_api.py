#!usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: python_api.py
# trying out writing a basic API

import bottle
import re
# import mysql.connector as mariadb

CHUNK_REGEX = "([A-Z][A-Z]):[0-1]\d:[0-6]\d:[0-7]\d:\d{3}"
MP_REGEX = "[0-1]\d:[0-6]\d:[0-7]\d:\d{3}"
books = {"1-Nephi": "01", "2-Nephi": "02", "Jacob": "03", "Enos": "04", "Jarom": "05",
             "Omni": "06", "Words of Mormon": "7", "Mosiah": "08", "Alma": "09", "Helaman": "10",
             "3-Nephi": "11", "4-Nephi": "12", "Mormon": "13", "Ether": "14", "Moroni": "15"}


@bottle.route('/<book>/<chapter>')
def get_chapter(book, chapter):
    """
    To return all chunks for the given chapter in JSON format

    :param book: (str) the book requested
    :param chapter: (str) the chapter in the book requested
    :return chapter_chunks: list of Chunks for the chapter requested
    """
    # TODO: Should this also return the corresponding info for the secondary language?
    pass

# No route since it is a helper function
def get_flipped_words():
    """
    Get list of all the words for the chapter that have already been flipped.
    Helper function for use in get_chapter()

    :return words: (list) Chunk uids to flip
    """
    pass


@bottle.route('/chunk/<uid>')
def get_one_chunk(uid):
    """
    Get one Chunk from the database and return it to the function caller.

    :param uid: (str) the uid for the Chunk requested.
    :return chunk: (Chunk) The Chunk with the uid specified in the function call.
    """
    pass


@bottle.route('/flip/<uid>')
def flip_one_chunk(uid):
    """
    Sets one Chunk as flipped in the database.

    :param uid: (str) The Chunk uid that needs to be set as flipped.
    :return confirm_flip: (tuple) (boolean, str/None)
            True to confirm it was flipped, False to indicate an error
            Error message if there was an error, None if no error
    """
    pass


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
    pass


@bottle.route('/prefs/<uid>/<p_lang>-<s_lang>')  # Not sure if this url format will work
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


def convert_url_to_uid(url):
    """
    Convert uids from the URL format to the normal format and verifies the uid is in the proper format

    :param url: The uid in URL format with the colons as %3A
    :return uid: Valid uid as long as url matches a proper uid once converted
    :return: None is returned if url isn't formatted properly once converted
    """
    mylist = url.split("%3A")
    uid = "{lang}:{book}:{chap}:{verse}:{pos}".format(lang=mylist[0], book=mylist[1], chap=mylist[2],
                                                      verse=mylist[4], pos=mylist[5])
    pattern = re.complie(CHUNK_REGEX)
    if pattern.match(uid) is True:
        return uid
    else:
        return None
