
# This mutator is for EMF files. See https://www.mcafee.com/blogs/other-blogs/mcafee-labs/analyzing-cve-2021-1665-remote-code-execution-vulnerability-in-windows-gdi/ and 

from parser import * # Import all of the stuff from the parser.
import random
from value_mut import * # This is for the actual mutation strategies. This implements mutate_tuple
import copy
import generic_mutator_bytes # This is for the generic mutation shit.
from debug import *
import record_types # This is for the EMR_NAMES which we use in the generation of random records.
import autogenerated # This is for the actual classes.
import os # For random bytes with urandom
import dummy_record

import pickle

# Put all mutation chances and constants here for now.

MUT_EXTRA_DATA_CHANCE = 0.8 # 3/10 chance to mutate the extra fields (if such exist.)
MUT_MIN_RAND_EXTRA_DATA_LEN = 10
MUT_MAX_RAND_EXTRA_DATA_LEN = 200


def load_dictionary():
	with open("dictionary.pkl", "rb") as f:
		objects = pickle.load(f)
	return objects


EMF_RECORD_DICTIONARY = load_dictionary() # Load the emf record dictionary.


def mut_field(rec) -> None:
	# Mutates a field in a record.
	available_fields = copy.deepcopy(rec.fields) # We need to do a copy here because otherwise we would modifying the object itself.
	assert "Size" in available_fields and "Type" in available_fields
	# Doesn't make sense to mutate these.
	available_fields.remove("Type")
	available_fields.remove("Size")
	if not available_fields: # Record only has the "Type" and "Size" fields.
		#debugprint("No fields...")
		return
	field = random.choice(available_fields)
	assert isinstance(field, str) # Should be string...
	field_tup = getattr(rec, field) # Get the actual attribute thing...
	# Now just do the thing...
	#debugprint("Mutating this field: "+str(field_tup))
	field_tup = mutate_tuple(field_tup)
	# Now set the mutated value to the object.
	setattr(rec, field, field_tup)
	return

def mutate_extra_data(record) -> None: # This function mutates extra data in 
	assert record.has_variable
	orig_data = copy.deepcopy(record.variable_data)
	orig_len = len(orig_data)
	new_data = generic_mutator_bytes.mutate_generic(orig_data) # Call the generic byte mutator
	# Now try to fix up the length field such that it works
	diff = len(new_data) - len(record.variable_data) # Difference
	assert len(record.variable_data) + diff == len(new_data)
	# Set the values
	record.variable_data = copy.deepcopy(new_data)
	assert hasattr(record, 'Size') # Should have the size stuff
	#record.Size[1] += diff # # TypeerROr: 'tuple' ObjeCT dOes nOT sUpport iTEm assIgnmenT
	record.Size = (record.Size[0], record.Size[1] + diff) # Add like this???
	# Double check..
	assert len(record.serialize()) == record.Size[1]
	# record.Size
	return



BANNED_REC_INTEGERS = [0x75, 69, 107]

def add_record_from_dictionary(obj: EMFFile) -> None: # Try adding a known good record from the dictionary stuff..
	random_record = copy.deepcopy(random.choice(EMF_RECORD_DICTIONARY)) # Just get a random good record.
	index = random.randint(0, len(obj.records))  # Random index in the range [0, len(lst)]
	obj.records.insert(index, random_record) # Insert the randomly generated value into the records in the object.
	return

def add_random_record(obj: EMFFile) -> None: # Generates a random record for this EMF file and appends it somewhere in the file.
	# Lookup a random record type.
	# If you look at https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-emf/1eec80ba-799b-4784-a9ac-91597d590ae1 the maximum record type is 0x7a .

	rec_type = random.randrange(2, 0x7a+1) # record type 1 is the header type, so don't bother generating another header.
	
	while rec_type in BANNED_REC_INTEGERS: # Some of these are banned.
		rec_type = random.randrange(2, 0x7a+1)
	rec_name = record_types.EMR_NAMES[rec_type] # This is the string representation of the thing.
	if not hasattr(autogenerated, rec_name): # Some bullshit happened.
		new_record = dummy_record.fake_record(rec_type) # Just create a fake record thing.

		index = random.randint(0, len(obj.records))  # Random index in the range [0, len(lst)]
		# print("added this record: "+str(rec_obj))
		obj.records.insert(index, copy.deepcopy(new_record)) # Insert the randomly generated value into the records in the object.
		return
	rec_class = getattr(autogenerated, rec_name) # Get the actual class.
	length = 8
	added_bytes = b"" # The bytes which we have added.
	while True:
		# autogenerated.
		# Try to initialize the record object. If this causes an exception, then we have the wrong number of bytes.
		all_bytes = struct.pack("I", rec_type) + struct.pack("I", length) + added_bytes
		assert len(all_bytes) == length # Should match.
		try:

			rec_obj = rec_class(all_bytes) # Try to initialize the thing...
		except:
			# Try to add a random byte maybe???
			added_bytes += bytes([random.randrange(0,256)]) # Add one byte.
			length += 1 # Add one.
			continue
		# No exception. We now have a (length-wise) valid record. Now we can check for extra data and add some if we want
		if rec_obj.has_variable:
			assert rec_obj.variable_data == b"" # Should be empty as of now.
			rand_data = os.urandom(random.randrange(MUT_MIN_RAND_EXTRA_DATA_LEN, MUT_MAX_RAND_EXTRA_DATA_LEN+1))
			rec_obj.variable_data = rand_data # Assign the extra data.
			# Fixup the length.
			diff = len(rand_data)
			rec_obj.Size = (rec_obj.Size[0], rec_obj.Size[1] + diff) # Fixup the length.
		break
	assert len(rec_obj.serialize()) == rec_obj.Size[1] # Should actually match.
	# Now add the newly generated record somewhere to the object.
	index = random.randint(0, len(obj.records))  # Random index in the range [0, len(lst)
	obj.records.insert(index, copy.deepcopy(rec_obj)) # Insert the randomly generated value into the records in the object.
	return


MAX_MUTATED_EXTRA_DATA_LENGTH = 20000 # Maximum length for the extra data stuff.


def modify_record(obj: EMFFile) -> None:
	rand_rec = random.choice(obj.records) # Just take some record from the object.
	# Now try to modify the stuff.
	# debugprint("Mutating this record: "+str(rand_rec))
	# Some of the mutation strategies are specific to records which have extra data.
	#print("BBBBBBBBBefore mutating: "+str(rand_rec))
	if rand_rec.has_variable and random.random() <= MUT_EXTRA_DATA_CHANCE: # Mutate extra data.
		mutate_extra_data(rand_rec)
		if len(rand_rec.variable_data) >= MAX_MUTATED_EXTRA_DATA_LENGTH:
			rand_rec.variable_data = rand_rec.variable_data[:MAX_MUTATED_EXTRA_DATA_LENGTH] # Just cut off the thing...
	else:
		mut_field(rand_rec)
	#print("After mutating: "+str(rand_rec))
	return

'''
def switch_fields(obj: EMFFile) -> None:
	debugprint("Switching records.")
	print("Switching records...")
	if len(obj.records) < 2:
		return # One or zero records.
	r1 = random.randrange(len(obj.mutable_fields()))# random.choice(obj.records)
	r2 = random.randrange(len(obj.mutable_fields()))# random.choice(obj.records)
	assert len(obj.mutable_fields()) == len(obj.fields) + 2 # This should always match..
	while r2 == r1: # Just pick a random one until be pick one which wasn't number two.
		r2 = random.randrange(len(obj.records))
	obj.fields[r1+2], obj.records[r2+2] = obj.records[r2+2], obj.records[r1+2] # Should swap the records. Plus two, because the first two are the type and size fields
	return
'''

# self.records


def switch_records(obj: EMFFile) -> None:
	#debugprint("Switching records.")
	#print("Switching records...")
	if len(obj.records) < 2:
		return # One or zero records.
	r1 = random.randrange(len(obj.records))# random.choice(obj.records)
	r2 = random.randrange(len(obj.records))# random.choice(obj.records)
	# assert len(obj.mutable_fields()) == len(obj.fields) + 2 # This should always match..
	while r2 == r1: # Just pick a random one until be pick one which wasn't number two.
		r2 = random.randrange(len(obj.records))
	obj.records[r1], obj.records[r2] = obj.records[r2], obj.records[r1] # Should swap the records. Plus two, because the first two are the type and size fields
	return

def shuffle_records(obj: EMFFile) -> None:
	print("Shuffled")
	if not obj.records:
		return
	random.shuffle(obj.records)
	return

RANDOM_RECORD_CHANCE = 0.05 # 5% chance of generating a completely random record.

def mutate_emf_obj(obj: EMFFile) -> None: # This modifies the structure in place. This is basically needed to mutate the structure in structure-aware ways such that we exercise the deep logic of the program.
	# Select mut strat.
	mut_strat = random.randrange(3) # This should always be zero. This is just so we can add more strategies later on...
	if mut_strat == 0:
		# Modify record.
		modify_record(obj)
	elif mut_strat == 1:
		# Switch records.
		switch_records(obj)
	#elif mut_strat == 2:
	#	shuffle_records(obj)
	#	# Try to modify the extra data
	elif mut_strat == 2: # Add a random, but valid record somewhere in the file.
		# Now try to actually do the stuff.
		if random.random() <= RANDOM_RECORD_CHANCE:

			add_random_record(obj)
		else:
			# Add a dictionary record, which we know to be good.
			add_record_from_dictionary(obj)
	else:
		print("Invalid mut strat")
		assert False

	return

def mutate_emf(emf_data): # This is the main mutation function. Takes an EMF file, parses it, modifies it and then serializes it back to bytes...
	emf_obj = parse_emf_file(emf_data)
	# Now mutate the thing
	mutate_emf_obj(emf_obj)
	# Fixup the header.
	fixup_header(emf_obj)
	ser_bytes = emf_obj.serialize()
	#print("Serialized bytes: "+str(ser_bytes))
	# assert len(header_bytes) == 108 # This because the header is extension 2
	ext_stuff = emf_obj.serialize_header() # Serialize the header.
	#print("Header seems to be the correct size...")
	return ext_stuff + ser_bytes # Return the header + records which should be a(n atleast somewhat) valid EMF file. 



def init(seed):
	pass


def fixup_header(obj: EMFFile) -> None: # This fixes the header of the object such that the structure is actually valid EMF.
	# fields = ['iType', 'nSize', 'rclBounds', 'rclFrame', 'dSignature', 'nVersion', 'nBytes', 'nRecords', 'nHandles', 'sReserved', 'nDescription', 'offDescription', 'nPalEntries', 'szlDevice', 'szlMillimeters', 'cbPixelFormat', 'offPixelFormat', 'bOpenGL', 'szlMicrometers']
	
	serialized_length = len(obj.serialize()) # Serialize for the length.
	assert hasattr(obj, 'h') # Should have the header attribute.
	header = obj.h
	assert hasattr(header, "nBytes")
	assert hasattr(header, "nRecords")
	header.nBytes = (header.nBytes[0], serialized_length)
	header.nRecords = (header.nRecords[0], len(obj.records)) # Should also have the correct number of records.
	assert serialized_length == len(obj.serialize()) # This should then match.
	return




def fuzz(buf):
	assert isinstance(buf, bytes) # Should be a bytearray
	orig_dat = copy.deepcopy(buf)





	orig_data = copy.deepcopy(buf)

	buf = bytes(buf)
	try:
		buf = mutate_emf(buf) # Mutate the EMF file...
		#if buf == orig_data: # Mutate generic.
		#	debugprint("The mutated data was the same!!!")
		#else:
		#	# Wasn not the same
		#	debugprint("The mutated data was NOT the same!!!")
		#return buf
		if buf == orig_data: # Mutate generic.
			return generic_mutator_bytes.mutate_generic(buf)
	except:
		buf = generic_mutator_bytes.mutate_generic(buf)
		return buf
		# return orig_data


	assert isinstance(buf, bytes)
	#buf = bytearray(buf) # Convert back to bytearray



	# Now just do this such that we don't overflow the buffer...
	# buf = buf[:max_size]
	return buf # Return the mutated buffer

TEST_MUT_COUNT = 200


SHOW_MUTATED = False

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
		# Write the data to a thing.
		if SHOW_MUTATED:
			fh = open("/mnt/c/Users/elsku/image.emf", "wb")
			fh.write(data)
			fh.close()
			# Now try to run the command.
			os.system("./RenderEMF.exe")
		orig_data2 = copy.deepcopy(data)
		data = mutate_emf(data)
		

		if data == orig_data:
			print("Mutated data was the same as original.")
			assert False

		###########else:
		#	print("Data was different!")

		#if len(data) != len(orig_data):
		#	print("LENGTH DIFFERS")

	return

import subprocess

def write_input(data):
	fh = open("/mnt/c/Users/elsku/image.emf", "wb")
	fh.write(data)
	fh.close()

def show_all_queue():
	directory = "/mnt/c/Users/elsku/outputs4/queue/"
	for file in os.listdir(directory): # For each file in the directory.
		print("file: "+str(file))
		if "id_" not in file:
			continue
		fh = open(directory+file, "rb")
		input_data = fh.read()
		fh.close()
		write_input(input_data) # Write the data to the file...
		# Run the thing.
		os.system("./RenderEMF.exe")


# debugprint("Initiefewfwefweeeeeeeeeeeed mutator!!!")


def load_data(filename):
	fh = open(filename, "rb")
	data = fh.read()
	fh.close()
	return data

def save_data(filename, data):
	fh = open(filename, "wb")
	fh.write(data)
	fh.close()
	return

GEN_HOW_MANY = 50000


def valid() -> bool:
	try:
		result = subprocess.run(["./checkvalidemf.exe", "testfile.emf"], capture_output=True, text=True, check=True)
	except:
		return False
	return True
	#output = result.stdout.strip()  # Strip any extra whitespace
	#print("output: "+str(output))
	#return False



def generate_corpus():
	initial_files = os.listdir("./initial/") # initial files....
	current_corpus = [load_data("./initial/"+file) for file in initial_files] # Load the initial data stuff.
	while len(current_corpus) < GEN_HOW_MANY: # Generate how many.
		random_selected = copy.deepcopy(random.choice(current_corpus))
		# Mutate
		random_selected = mutate_emf(random_selected)
		# Save to input.
		save_data("testfile.emf", random_selected)
		# Valid?
		if valid():
			# Save valid data to our corpus.
			current_corpus.append(copy.deepcopy(random_selected))
			print("Current corpus length: "+str(len(current_corpus)))
		# Check for automatic stop.
		stop = load_data("manual_stop")
		if stop == b"stop\n":
			break # Automatic stop.

	# Save each file to corpus directory.
	for i, data in enumerate(current_corpus):
		fh = open("./corpus/"+str(i), "wb")
		fh.write(data)
		fh.close()

	return


if __name__=="__main__":
	test_mut()
	# show_all_queue()
	# generate_corpus()
	exit(0)
