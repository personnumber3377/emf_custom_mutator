
import cparsing.emfheader # This is the automatically generated bullshit.
import copy
# emfheader_ext2.py
import cparsing.emfheader_ext2
TEST_FILE_NAME = "DrawString.emf"

def read_header(data):
	# EmfHeader 
	# https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-emf/80c0684b-9a0e-4bdb-8d6d-0e5a9e9673e7
	orig_data = copy.deepcopy(data)
	header_object = cparsing.emfheader.ParsedHeader(data)
	print("Here is the header: "+str(header_object))
	#restofdata = header_object.remaining_data # This is actually now wrong, because we changed the way this parses the bullshit. See the readme in the other repo.
	# len_rest = len(restofdata)
	#print("Rest of data: "+str(restofdata))
	# Now read the bullshit...
	print("header_object.nSize == "+str(header_object.nSize))
	if header_object.nSize[1] >= 108: # Extension 2 # Index at 1 is the actual value. The value at index 0 is the length of the actual value which is index 1
		print("Extension 2...")
		print("Size: "+str(header_object.nSize))
		header_object = cparsing.emfheader_ext2.ParsedHeader(data)
		# Sanity checking...
		print("Here is the header: "+str(header_object))
		assert header_object.sReserved[1] == 0 # Should be zero...
		
		#restofdata = header_object.remaining_data
		# Now try to see the thing
		serialized_data = header_object.serialize() # Try to serialize object back...
		# Compare the original data and serialized data. Should be the same.
		print("Header bytes:")
		# assert len_rest == len(orig_data) - header_object.nSize[1]
		print(serialized_data)
		assert serialized_data == orig_data[:header_object.nSize[1]] # Cut first header_object.nSize[1] bytes, because that is the actual value of the header...
		print("Actual rest of data: "+str(orig_data[header_object.nSize[1]:]))
		rest_of_data = orig_data[header_object.nSize[1]:]
		print("Test succeeded!")
		return header_object, rest_of_data # Return the rest of the data here too.
		# return restofdata
	elif header_object.nSize[1] >= 100: # Extension 1
		print("Extension 1...")
		print("Size: "+str(header_object.nSize))
		return
	else:
		print("Normal...")
		return
	return

def test_read_header():
	fh = open(TEST_FILE_NAME, "rb")
	data = fh.read()
	fh.close()
	header = read_header(data)
	return

if __name__=="__main__":
	test_read_header()
	exit(0)
