
import struct

class fake_record_other:
	has_variable = True
	fields = ["Type", "Size"]
	def __init__(self, bytes_stuff):

		type_and_size = bytes_stuff[:8]
		# self.Type, self.Size = struct.unpack('II', type_and_size) # Unpack two little endian integers.
		Type_int, Size_int = struct.unpack('II', type_and_size)
		self.Type = (4, Type_int)
		self.Size = (4, Size_int)
		# self.Type = type
		# self.Size = 8
		restofdata = bytes_stuff[8:]
		# Set the rest of the data
		self.has_variable = True
		self.variable_data = restofdata
		# self.otherdata = restofdata # Show the stuff.
		return

	def serialize(self):
		return struct.pack("I", self.Type[1]) + struct.pack("I", self.Size[1]) + self.variable_data


