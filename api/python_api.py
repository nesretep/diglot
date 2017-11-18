#!usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: python_api.py
# trying out writing a basic API

import bottle
import re
import mysql.connector as mariadb

CHUNK_REGEX = "([A-Z][A-Z]):[0-1][0-9]:[0-6][0-9]:[0-7][0-9]:\d{3}"
MP_REGEX = "[0-1][0-9]:[0-6][0-9]:[0-7][0-9]:\d{3}"


@bottle.route('/<book_id>/<chapter_id>')
def get_chapter(chapter_id):
    """
    To return all chunks for the given chapter in JSON format

    :param chapter_id (str): similar to chunk ID, format: EN:#:#:#:#
    :return chapter: list of Chunks for the chapter requested
    """
    pass


def get_flipped_words():
    """
    Get list of all the words for the chapter that have already been flipped.

    :return words (list): list of Chunk uids to flip
    """
    pass


def get_one_word(uid):
    """
    Get one Chunk from the database.

    :param uid (str): the uid for the Chunk requested.
    :return chunk (Chunk): The Chunk with the uid specified in the function call.
    """
    pass


def flip_one_chunk(uid):
    """
    Sets one Chunk as flipped in the database.

    :param uid (str): The Chunk uid that needs to be set as flipped.
    :return confirm_flip (tuple): (boolean, str/None)
            True to confirm it was flipped, False to indicate an error
            Error message if there was an error, None if no error
    """
    pass


def set_flipped_list(chunks):
    """
    Updates the database with Chunks that were flipped in that session

    :param chunks (list):
    :return confirm_list_set (tuple): (boolean, str/None)
            True to indicate update was successful, False if error
            Error message if there was an error, None if no error
    """
    pass

def past_critical_point():
    """
    Checks if user is past critical point

    :return critical (boolean): True if past critical point, False if not
    """
    pass


def set_user_level(level):
    """
    Sets the user's level in their user preferences.

    :param level (int): Indicates the difficulty the user is comfortable with
    :return confirm_level_set (tuple): (boolean, str/None)
            True to indicate update was successful, False if error
            Error message if there was an error, None if no error
    """
    pass


def set_user_language(p_lang, s_lang):
    """
    Sets the user's language preferences.

    :param p_lang (str): 2 character ISO designation for the user's primary language.
    :param s_lang (str): 2 character ISO designation for the user's secondary language.
    :return confirm_lang_set (tuple): (boolean, str/None)
            True to indicate update was successful, False if error
            Error message if there was an error, None if no error
    """
    pass
