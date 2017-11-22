#!usr/bin/env python3
# -*- coding: utf-8 -*-

import ConfigParser
import pymysql as mariadb
import sqlalchemy
import logging


def connect_to_db(connect_type, config_path):
    """
    Connects to the database defined in the configuration file given

    :param connect_type: (str) tells which connection method to use to connect to the db (either mariadb or sqlalchemy)
    :param config_path: (str) the path to the configuration file
    :return: connection object for the connection type specified in connect_type
    """
    config = ConfigParser.SafeConfigParser()
    config.read(config_path)  # do we want to just hard code the file path rather than passing it in?
    username = config.get('database', 'username')
    password = config.get('database', 'password')
    database = config.get('database', 'database')
    hostname = config.get('database', 'hostname')

    if connect_type == "mariadb":
        dbconnect = mariadb.connect(host=hostname, user=username, passwd=password, db=database)
        return dbconnect
    elif connect_type == "sqlalchemy":
        engine = sqlalchemy.create_engine('mysql+pymysql://{}:{}@{}/{}'.format(username, password, hostname, database))
        return engine


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