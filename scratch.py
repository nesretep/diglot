# Possible JSON Structures represented as Python Dicts/Lists

# One Chunk:
{
	"uid": "EN:1:1:1:1",
	"value": "Blah Blah Blah",
	"flip_status": 0
	"audio_clip_url": 
	"definition": "This word means this."
}

# Chapter:
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
			flip_status (int)    : 0 represents not flipped, 1 represents flipped, 2 represents suggested(?)

		For future implementation:
			definition (str)     : The text of the definition of the chunk
			audio_clip_url (str) : URL where the audio clip for the chunk is located
	"""

	
	def __cmp__(self, other):
		if self.pos > other.pos:
			return 1
		elif self.pos < other.pos:
			return -1
		else:
			return 0


	def __init__(self, uid, value, flip_status=0, definition=None, audio_clip_url=None):
		self.uid = uid
		self.value = value
		self.flip_status = flip_status
		self.definition = definition
		self.audio_clip_url = audio_clip_url


	def to_dict(self):
		return object.__dict__


	# I don't know if these would be helpful or not.
	pos = self.uid.split(":")[4]
	verse = self.uid.split(":")[3]
	chapter = self.uid.split(":")[2]
	book = self.uid.split(":")[1]
	lang = self.uid.split(":")[0]
