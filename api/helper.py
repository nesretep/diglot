#!usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import pymysql as mariadb
import re
import logging
import bottle
import datetime

INSTANCE_REGEX = "[a-z]{3}:[0-1]\d:[0-6]\d:[0-7]\d:\d{3}"
MP_REGEX = "[0-1]\d:[0-6]\d:[0-7]\d:\d{3}"
CP_REGEX = "[a-z]{3}:[0-1]\d:[0-6]\d"


def connect_to_db(config_path, adminuser=False):
    """
    Connects to the database defined in the configuration file given

    :param config_path: (str) the path to the configuration file
    :param adminuser: (boolean) indicates whether to connect to the database with the admin user or not
    :return: connection object for the connection type specified in connect_type
    """
    config = configparser.ConfigParser()
    config.read(config_path)
    database = config['database']['database']
    hostname = config['database']['hostname']
    charset = config['database']['charset']

    if adminuser is True:
        username = config['admin']['username']
        password = config['admin']['password']
    else:
        username = config['api']['username']
        password = config['api']['password']

    try:
        dbconnect = mariadb.connect(host=hostname, user=username, passwd=password, db=database, charset=charset)
        logging.info("Connected to {} database successfully using {} user.".format(database, username))
        return dbconnect
    except mariadb.Error as dberror:
        msg = "{}: Unable to connect to database: {}".format(datetime.datetime.now(), dberror)
        logging.error(msg)
        bottle.response.status = 500


def is_valid_uid(uid, id_type):
    """
    Validator function to make sure uids are in the proper format by checking against regex

    :param uid: (str) the uid to validate
    :param id_type: (str) type of uid pattern to check against - instance or master position (mp)
    :return: (bool) result of the regex pattern checking against the pattern specified by 'type'
    """
    instance_pattern = re.compile(INSTANCE_REGEX)
    mp_pattern = re.compile(MP_REGEX)
    cp_pattern = re.compile(CP_REGEX)
    if id_type.lower() == "instance":
        return bool(instance_pattern.match(uid))
    elif id_type.lower() == "mp":
        return bool(mp_pattern.match(uid))
    elif id_type.lower() == "cp":
        return bool(cp_pattern.match(uid))
    else:
        return None


def is_valid_lang(lang_id):
    """
    Validates language ids against the specified regex

    :param lang_id: (str) the language id passed in to the function to be validated
    :return: (bool) result of the regex checking against the pattern
    """
    lang_id_pattern = re.compile("[a-z]{3}")
    return bool(lang_id_pattern.match(lang_id))


def is_valid_concept(concept_id):
    """
    Validates concept ids against their matching regex

    :param concept_id: (str) the concept id to validate
    :return: (bool) result of the regex checking against the pattern
    """
    concept_id_pattern = re.compile("[a-z]{3}_con_[0-9]{5}")
    return bool(concept_id_pattern.match(concept_id))


def is_injection(query):
    """
    Checks query for characters commonly used in SQL injection attacks.

    :param query: (str) The query being checked.
    :return: (bool) True if the unacceptable character are found, False if they are not found
    """
    pattern = re.compile("^[^<>;]*$")
    return not bool(pattern.match(query))
