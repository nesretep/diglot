#! usr/bin/env python3
# filename: python_api.py
# trying out writing a basic API

import requests
import mysql.connector as mariadb


def get_chapter(chapter_id):
    """
    To return all chunks for the given chapter in JSON format

    :param chapter_id (str): similar to chunk ID, format: EN:#:#:#:#
    :return chapter: list of Chunks for the chapter requested
    """
    pass


def flip_words():
    """
    Flip all the words for the chapter that have already been flipped.
    
    :return flipme (list): list of Chunk uids to flip
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
    :return:
    """
    pass


def set_flipped_list(chunks):
    """
    Updates the database with Chunks that were flipped in that session

    :param uid:
    :return:
    """
    pass

def past_critical_point():
    """
    Checks if user is past critical point

    :return critical (boolean): True if past critical point, False if not
    """
    pass
