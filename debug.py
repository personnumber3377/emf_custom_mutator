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


