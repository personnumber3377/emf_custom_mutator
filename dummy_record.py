
import struct

class fake_record:
	def __init__(self, type):
		self.Type = type
		self.Size = 8
	def serialize(self):
		return struct.pack("I", self.Type) + struct.pack("I", self.Size)
