#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Chunk object class definition

class Chunk(object):
    """
        Class object for a chunk of text

        Attributes:
            uid (str)         : the unique ID of the chunk in the format LANG:##:##:##:###
            text (str)        : the actual Book of Mormon text of the chunk
            masterpos (str)   : master position this Chunk is connected to
            flipped (bool)    : False represents not flipped, True represents flipped
            tag (dict)        : dict holding the boolean value for each of the different tag types
            rank (int)        : the number representing the difficulty of the Chunk
            pos (int)         : the in-verse natural position of the Chunk
            verse (int)       : the verse the Chunk is in
            chapter (int)     : the chapter the Chunk is in
            book (int)        : a numeric representation of the book the Chunk is in with 1 Nephi being 1 and so on
            lang (str)        : the two-letter ISO designation for the language the Chunk is in
            suggested (int)   : 0- not suggested, 1- suggested, 2- suggested, but not flipped
    """
    def __init__(self, uid, text, masterpos, rank, flipped, tag, suggested):
        self.uid = uid
        self.text = text
        self.masterpos = masterpos
        self.rank = rank
        self.flipped = flipped
        self.tag = tag
        self.suggested = suggested
        # self.cf_id = cf_id

        self.pos = int(self.uid.split(":")[4])
        self.verse = int(self.uid.split(":")[3])
        self.chapter = int(self.uid.split(":")[2])
        self.book = int(self.uid.split(":")[1])
        self.lang = self.uid.split(":")[0]


    def __cmp__(self, other):
        """
        Comparison function for the class; compares based on in-verse position

        :param other: (Chunk Object) other chunk object being compared
        :return (int)     : number that indicates which is greater
        """
        if self.verse > other.verse:
            return 1
        elif self.verse < other.verse:
            return -1
        else:
            if self.pos > other.pos:
                return 1
            elif self.pos < other.pos:
                return -1
            else:
                return 0

    def to_dict(self):
        return self.__dict__
