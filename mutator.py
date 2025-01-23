
# This mutator is for EMF files. See https://www.mcafee.com/blogs/other-blogs/mcafee-labs/analyzing-cve-2021-1665-remote-code-execution-vulnerability-in-windows-gdi/ and 

from parser import * # Import all of the stuff from the parser.
import random
from value_mut import * # This is for the actual mutation strategies. This implements mutate_tuple
import copy
import generic_mutator_bytes # This is for the generic mutation shit.

def mut_field(rec) -> None:
	# Mutates a field in a record.
	available_fields = copy.deepcopy(rec.fields) # We need to do a copy here because otherwise we would modifying the object itself.
	assert "Size" in available_fields and "Type" in available_fields
	# Doesn't make sense to mutate these.
	available_fields.remove("Type")
	available_fields.remove("Size")
	if not available_fields: # Record only has the "Type" and "Size" fields.
		return
	field = random.choice(available_fields)
	assert isinstance(field, str) # Should be string...
	field_tup = getattr(rec, field) # Get the actual attribute thing...
	# Now just do the thing...
	field_tup = mutate_tuple(field_tup)
	# Now set the mutated value to the object.
	setattr(rec, field, field_tup)
	return

def modify_record(obj: EMFFile) -> None:
	rand_rec = random.choice(obj.records) # Just take some record from the object.
	# Now try to modify the stuff.
	mut_field(rand_rec)
	return

def mutate_emf_obj(obj: EMFFile) -> None: # This modifies the structure in place. This is basically needed to mutate the structure in structure-aware ways such that we exercise the deep logic of the program.
	# Select mut strat.
	mut_strat = random.randrange(1) # This should always be zero. This is just so we can add more strategies later on...

	if mut_strat == 0:
		# Modify record.
		modify_record(obj)
	else:
		print("Invalid mut strat")
		assert False
	return

def mutate_emf(emf_data): # This is the main mutation function. Takes an EMF file, parses it, modifies it and then serializes it back to bytes...
	emf_obj = parse_emf_file(emf_data)
	# Now mutate the thing
	mutate_emf_obj(emf_obj)
	ser_bytes = emf_obj.serialize()
	print("Serialized bytes: "+str(ser_bytes))
	# assert len(header_bytes) == 108 # This because the header is extension 2
	ext_stuff = emf_obj.serialize_header() # Serialize the header.
	print("Header seems to be the correct size...")
	return ext_stuff + ser_bytes # Return the header + records which should be a(n atleast somewhat) valid EMF file. 



def init(seed):
	pass


def debugprint(string):
	fh = open("C:\\Users\\elsku\\debugging.txt", "a")
	fh.write(string)
	fh.write("\n")
	fh.close()
	return


# def fuzz(buf, add_buf, max_size):
#def fuzz(buf, buf_size):

def hexdump(data: bytes, group_size=1, bytes_per_line=16): # Thanks ChatGPT
	offset = 0
	for i in range(0, len(data), bytes_per_line):
		# Slice a line of bytes
		line = data[i:i + bytes_per_line]
		
		# Format the offset as a 6-character hex value
		offset_str = f"{offset:08x}"
		
		# Create a hexdump line with grouped bytes
		hex_bytes = " ".join(f"{byte:02x}" for byte in line)
		
		# Add the ASCII representation
		ascii_bytes = "".join(chr(byte) if 32 <= byte <= 126 else "." for byte in line)
		
		# Print the full line
		print(f"{offset_str}: {hex_bytes:<{3 * bytes_per_line}} {ascii_bytes}")
		offset += bytes_per_line


# debugprint
def hexdumpdebug(data: bytes, group_size=1, bytes_per_line=16): # Thanks ChatGPT
	offset = 0
	for i in range(0, len(data), bytes_per_line):
		# Slice a line of bytes
		line = data[i:i + bytes_per_line]
		
		# Format the offset as a 6-character hex value
		offset_str = f"{offset:08x}"
		
		# Create a hexdump line with grouped bytes
		hex_bytes = " ".join(f"{byte:02x}" for byte in line)
		
		# Add the ASCII representation
		ascii_bytes = "".join(chr(byte) if 32 <= byte <= 126 else "." for byte in line)
		
		# Print the full line
		debugprint(f"{offset_str}: {hex_bytes:<{3 * bytes_per_line}} {ascii_bytes}")
		offset += bytes_per_line


def fuzz(buf):
	debugprint("Called theeeee mutator!!!!!")
	assert isinstance(buf, bytes) # Should be a bytearray
	orig_dat = copy.deepcopy(buf)
	print("="*20)
	print("Original data here:")
	hexdump(orig_dat)
	print("="*20)


	debugprint("="*20)
	debugprint("Original data here:")
	hexdumpdebug(buf)
	debugprint("="*20)

	debugprint("2!!!!!")


	orig_data = copy.deepcopy(buf)

	buf = bytes(buf)
	try:
		buf = mutate_emf(buf) # Mutate the EMF file...
		if buf == orig_data: # Mutate generic.
			return generic_mutator_bytes.mutate_generic(buf)
	except:
		debugprint("EMF mutation failed!!!!! Falling back to generic mutator!")
		debugprint("Type of buffer before: "+str(type(buf)))
		buf = generic_mutator_bytes.mutate_generic(buf)
		debugprint("Type of buffer after: "+str(type(buf)))
		debugprint("Returning the generic mutated data.")
		return buf
	print("="*20)
	print("After mutation:")
	hexdump(buf)
	print("="*20)

	debugprint("="*20)
	debugprint("After mutation:")
	hexdumpdebug(buf)
	debugprint("="*20)

	debugprint("3!!!!!")
	assert isinstance(buf, bytes)
	debugprint("4!!!!!")
	#buf = bytearray(buf) # Convert back to bytearray
	debugprint("4!!!!!")



	# Now just do this such that we don't overflow the buffer...
	# buf = buf[:max_size]
	return buf # Return the mutated buffer

TEST_MUT_COUNT = 100

def test_mut():

	fh = open(TEST_FILE_NAME, "rb")
	data = fh.read()
	fh.close()
	orig_data = copy.deepcopy(data)
	# Now parse header...
	# h, rest_of_data = parse_header(data)
	# Now try to parse the records
	# records = parse_records(rest_of_data) # Try to parse the records from the data.
	for _ in range(TEST_MUT_COUNT):
		orig_data = copy.deepcopy()
		data = mutate_emf(data)

	return

debugprint("Initiefewfwefweeeeeeeeeeeed mutator!!!")

if __name__=="__main__":
	test_mut()
	exit(0)
