#!usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import pymysql as mariadb
import re
import logging
CHUNK_REGEX = "[A-Z]{3}:[0-1]\d:[0-6]\d:[0-7]\d:\d{3}"
MP_REGEX = "[0-1]\d:[0-6]\d:[0-7]\d:\d{3}"


def connect_to_db(config_path, adminuser=False):
    """
    Connects to the database defined in the configuration file given

    :param config_path: (str) the path to the configuration file
    :param adminuser: (boolean) indicates whether to connect to the database with the admin user or not
    :return: connection object for the connection type specified in connect_type
    """
    config = configparser.ConfigParser()
    config.read(config_path)  # do we want to just hard code the file path rather than passing it in?
    database = config['database'][ 'database']
    hostname = config['database']['hostname']
    if adminuser is True:
        username = config['admin']['username']
        password = config['admin']['password']
    else:
        username = config['api']['username']
        password = config['api']['password']

    try:
        dbconnect = mariadb.connect(host=hostname, user=username, passwd=password, db=database)
        return dbconnect
    except Exception as dberror:
        raise


def convert_url_to_uid(url):
    """
    Convert uids from the URL format to the normal format and verifies the uid is in the proper format

    :param url: (str) The uid in URL format with the colons as %3A
    :return uid: (str) Valid uid as long as url matches a proper uid once converted
    :return: None is returned if url isn't formatted properly once converted
    """
    mylist = url.split("%3A")
    uid = "{lang}:{book}:{chap}:{verse}:{pos}".format(lang=mylist[0], book=mylist[1], chap=mylist[2],
                                                      verse=mylist[4], pos=mylist[5])
    if is_valid_uid(uid) is True:
        return uid
    else:
        return None


def is_valid_uid(uid, type):
    """
    Validator function to make sure uids are in the proper format

    :param uid: (str) the uid to validate
    :param type: type of uid pattern to check against
    :return: result of the regex pattern checking (True/False) against the pattern specified by 'type'
    """
    chunk_pattern = re.compile(CHUNK_REGEX)
    mp_pattern = re.compile(MP_REGEX)
    if type.lower() == "chunk":
        return bool(chunk_pattern.match(uid))
    elif type.lower() == "mp":
        return bool(mp_pattern.match(uid))
    else:
        return None


def check_login(username, password):
    """
    This is a placerholder function for some sort af actual authentication setup.

    :param username: username of user being authenticated
    :param password: the user's password
    :return: boolean indicating the success or failure of the login attempt
    """
    return True



