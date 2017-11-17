# Possible JSON Structures represented as Python Dicts/Lists

# One Chunk:
Chunk1 = {"uid": "EN:1:1:1:1",
          "value": "Blah Blah Blah",
          "flip_status": 0}

 Chapter:
{
    {
        Chunk
    },
    {
        Chunk
    },
    .
    .
    .
    {
        last Chunk
    }
}

class Chunk(object):
    """
        Class for a chunk of text

        Attributes:
            uid (str)            : the unique ID of the chunk in the format LANG:#:#:#:#
            value (str)          : the actual Book of Mormon text of the chunk
            masterpos (str)      : master position this Chunk is connected to
            flip_status (int)    : 0 represents not flipped, 1 represents flipped, 2 represents suggested(?)
            pos (int)            : the in-verse natural position of the Chunk
            verse (int)          : the verse the Chunk is in
            chapter (int)        : the chapter the Chunk is in
            book (int)           : a numeric representation of the book the Chunk is in with 1 Nephi being 1 and so on
            lang (str)           : the two-letter ISO designation for the language the Chunk is in
    """
    def __init__(self, uid, value, masterpos, flip_status=0):
        self.uid = uid
        self.value = value
        self.flip_status = flip_status
        self.masterpos = masterpos
        # I don't know if these would be helpful or not.
        self.pos = int(self.uid.split(":")[4])
        self.verse = int(self.uid.split(":")[3])
        self.chapter = int(self.uid.split(":")[2])
        self.book = int(self.uid.split(":")[1])
        self.lang = self.uid.split(":")[0]


    def __cmp__(self, other):
        """
        Comparison function for the class; compares based on in-verse position

        :param other (int): position value from other object
        :return (int)     : number that indicates which is greater
        """
        if self.pos > other.pos:
            return 1
        elif self.pos < other.pos:
            return -1
        else:
            return 0





