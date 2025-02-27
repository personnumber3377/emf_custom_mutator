#!/bin/sh

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
import os
from emf_file import * # For parsing the stuff.
import pickle

# This file is supposed to generate a dictionary of known good records from a list of known good EMF files for the fuzzer to use.

KNOWN_GOOD_DIR = "./knowngood/"

def read_file(fn):
	fh = open(fn, "rb")
	data = fh.read()
	fh.close()
	return data

def gen_dict():
	output_records = []
	known_good_files = os.listdir(KNOWN_GOOD_DIR)
	for file in known_good_files:
		emf_data = read_file(KNOWN_GOOD_DIR+file) # Read the file.
		# Now try to parse it...
		parsed_object = parse_emf_file(emf_data)

		# Now get the records and add them to the output list maybe?????
		output_records.extend(parsed_object.records) # Add the records like this maybe???

	# Now we have a big list of known interesting records, so just pickle them to a file maybe???

	print("Length of all of the records: "+str(len(output_records)))

	with open("dictionary.pkl", "wb") as f:
		pickle.dump(output_records, f)
	print("[+] Done!")


'''
with open("data.pkl", "rb") as f:
    objects = pickle.load(f)
'''

if __name__=="__main__":

	gen_dict()
	exit(0)
