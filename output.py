import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer


import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '24b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Bounds', 'xDest', 'yDest', 'cxDest', 'cyDest', 'BLENDFUNCTION', 'xSrc', 'ySrc', 'XformSrc', 'BkColorSrc', 'UsageSrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc', 'cxSrc', 'cySrc']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Bounds', 'xDest', 'yDest', 'cxDest', 'cyDest', 'BLENDFUNCTION', 'xSrc', 'ySrc', 'XformSrc', 'BkColorSrc', 'UsageSrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc', 'cxSrc', 'cySrc']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Bounds', 'xDest', 'yDest', 'cxDest', 'cyDest', 'BLENDFUNCTION', 'xSrc', 'ySrc', 'XformSrc', 'BkColorSrc', 'UsageSrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc', 'cxSrc', 'cySrc'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '24b', '4b', '4b', '4b', '4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Bounds', 'xDest', 'yDest', 'cxDest', 'cyDest', 'BitBltRasterOperation', 'xSrc', 'ySrc', 'XformSrc', 'BkColorSrc', 'UsageSrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Bounds', 'xDest', 'yDest', 'cxDest', 'cyDest', 'BitBltRasterOperation', 'xSrc', 'ySrc', 'XformSrc', 'BkColorSrc', 'UsageSrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Bounds', 'xDest', 'yDest', 'cxDest', 'cyDest', 'BitBltRasterOperation', 'xSrc', 'ySrc', 'XformSrc', 'BkColorSrc', 'UsageSrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '4b', '4b', '4b', '4b', '4b', '2b', '4b', '4b', '24b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Bounds', 'xDest', 'yDest', 'cxDest', 'cyDest', 'ROP4', 'Reserved', 'xSrc', 'ySrc', 'XformSrc', 'BkColorSrc', 'UsageSrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc', 'xMask', 'yMask', 'UsageMask', 'offBmiMask', 'cbBmiMask', 'offBitsMask', 'cbBitsMask']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Bounds', 'xDest', 'yDest', 'cxDest', 'cyDest', 'ROP4', 'Reserved', 'xSrc', 'ySrc', 'XformSrc', 'BkColorSrc', 'UsageSrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc', 'xMask', 'yMask', 'UsageMask', 'offBmiMask', 'cbBmiMask', 'offBitsMask', 'cbBitsMask']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Bounds', 'xDest', 'yDest', 'cxDest', 'cyDest', 'ROP4', 'Reserved', 'xSrc', 'ySrc', 'XformSrc', 'BkColorSrc', 'UsageSrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc', 'xMask', 'yMask', 'UsageMask', 'offBmiMask', 'cbBmiMask', 'offBitsMask', 'cbBitsMask'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '24b', '4b', '4b', '4b', '4b', '24b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Bounds', 'aptlDest', 'xSrc', 'ySrc', 'cxSrc', 'cySrc', 'XformSrc', 'BkColorSrc', 'UsageSrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc', 'xMask', 'yMask', 'UsageMask', 'offBmiMask', 'cbBmiMask', 'offBitsMask', 'cbBitsMask']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Bounds', 'aptlDest', 'xSrc', 'ySrc', 'cxSrc', 'cySrc', 'XformSrc', 'BkColorSrc', 'UsageSrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc', 'xMask', 'yMask', 'UsageMask', 'offBmiMask', 'cbBmiMask', 'offBitsMask', 'cbBitsMask']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Bounds', 'aptlDest', 'xSrc', 'ySrc', 'cxSrc', 'cySrc', 'XformSrc', 'BkColorSrc', 'UsageSrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc', 'xMask', 'yMask', 'UsageMask', 'offBmiMask', 'cbBmiMask', 'offBitsMask', 'cbBitsMask'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Bounds', 'xDest', 'yDest', 'xSrc', 'ySrc', 'cxSrc', 'cySrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc', 'UsageSrc', 'iStartScan', 'cScans']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Bounds', 'xDest', 'yDest', 'xSrc', 'ySrc', 'cxSrc', 'cySrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc', 'UsageSrc', 'iStartScan', 'cScans']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Bounds', 'xDest', 'yDest', 'xSrc', 'ySrc', 'cxSrc', 'cySrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc', 'UsageSrc', 'iStartScan', 'cScans'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '24b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Bounds', 'xDest', 'yDest', 'cxDest', 'cyDest', 'BitBltRasterOperation', 'xSrc', 'ySrc', 'XformSrc', 'BkColorSrc', 'UsageSrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc', 'cxSrc', 'cySrc']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Bounds', 'xDest', 'yDest', 'cxDest', 'cyDest', 'BitBltRasterOperation', 'xSrc', 'ySrc', 'XformSrc', 'BkColorSrc', 'UsageSrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc', 'cxSrc', 'cySrc']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Bounds', 'xDest', 'yDest', 'cxDest', 'cyDest', 'BitBltRasterOperation', 'xSrc', 'ySrc', 'XformSrc', 'BkColorSrc', 'UsageSrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc', 'cxSrc', 'cySrc'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Bounds', 'xDest', 'yDest', 'xSrc', 'ySrc', 'cxSrc', 'cySrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc', 'UsageSrc', 'BitBltRasterOperation', 'cxDest', 'cyDest']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Bounds', 'xDest', 'yDest', 'xSrc', 'ySrc', 'cxSrc', 'cySrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc', 'UsageSrc', 'BitBltRasterOperation', 'cxDest', 'cyDest']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Bounds', 'xDest', 'yDest', 'xSrc', 'ySrc', 'cxSrc', 'cySrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc', 'UsageSrc', 'BitBltRasterOperation', 'cxDest', 'cyDest'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '24b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Bounds', 'xDest', 'yDest', 'cxDest', 'cyDest', 'TransparentColor', 'xSrc', 'ySrc', 'XformSrc', 'BkColorSrc', 'UsageSrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc', 'cxSrc', 'cySrc']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Bounds', 'xDest', 'yDest', 'cxDest', 'cyDest', 'TransparentColor', 'xSrc', 'ySrc', 'XformSrc', 'BkColorSrc', 'UsageSrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc', 'cxSrc', 'cySrc']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Bounds', 'xDest', 'yDest', 'cxDest', 'cyDest', 'TransparentColor', 'xSrc', 'ySrc', 'XformSrc', 'BkColorSrc', 'UsageSrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc', 'cxSrc', 'cySrc'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Clip']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Clip']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Clip'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'RgnDataSize', 'RegionMode']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'RgnDataSize', 'RegionMode']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'RgnDataSize', 'RegionMode'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Clip']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Clip']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Clip'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '8b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Offset']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Offset']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Offset'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'RegionMode']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'RegionMode']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'RegionMode'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'CommentIdentifier']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'CommentIdentifier']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'CommentIdentifier'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'CommentIdentifier', 'EMFSpoolRecordIdentifier']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'CommentIdentifier', 'EMFSpoolRecordIdentifier']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'CommentIdentifier', 'EMFSpoolRecordIdentifier'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'nPalEntries', 'offPalEntries', 'SizeLast']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'nPalEntries', 'offPalEntries', 'SizeLast']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'nPalEntries', 'offPalEntries', 'SizeLast'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '8b', '4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Center', 'Radius', 'StartAngle', 'SweepAngle']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Center', 'Radius', 'StartAngle', 'SweepAngle']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Center', 'Radius', 'StartAngle', 'SweepAngle'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '8b', '8b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Box', 'Start', 'End']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Box', 'Start', 'End']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Box', 'Start', 'End'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '8b', '8b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Box', 'Start', 'End']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Box', 'Start', 'End']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Box', 'Start', 'End'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '8b', '8b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Box', 'Start', 'End']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Box', 'Start', 'End']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Box', 'Start', 'End'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Box']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Box']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Box'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '8b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Start', 'Color', 'FloodFillMode']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Start', 'Color', 'FloodFillMode']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Start', 'Color', 'FloodFillMode'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Bounds', 'iGraphicsMode', 'exScale', 'eyScale']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Bounds', 'iGraphicsMode', 'exScale', 'eyScale']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Bounds', 'iGraphicsMode', 'exScale', 'eyScale'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Bounds', 'iGraphicsMode', 'exScale', 'eyScale']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Bounds', 'iGraphicsMode', 'exScale', 'eyScale']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Bounds', 'iGraphicsMode', 'exScale', 'eyScale'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Bounds']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Bounds']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Bounds'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Bounds', 'RgnDataSize', 'ihBrush']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Bounds', 'RgnDataSize', 'ihBrush']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Bounds', 'RgnDataSize', 'ihBrush'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '4b', '4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Bounds', 'RgnDataSize', 'ihBrush', 'Width', 'Height']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Bounds', 'RgnDataSize', 'ihBrush', 'Width', 'Height']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Bounds', 'RgnDataSize', 'ihBrush', 'Width', 'Height'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Bounds', 'nVer', 'nTri', 'ulMode']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Bounds', 'nVer', 'nTri', 'ulMode']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Bounds', 'nVer', 'nTri', 'ulMode'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '8b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Point']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Point']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Point'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Bounds', 'RgnDataSize']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Bounds', 'RgnDataSize']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Bounds', 'RgnDataSize'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '8b', '8b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Box', 'Start', 'End']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Box', 'Start', 'End']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Box', 'Start', 'End'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Bounds', 'Count']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Bounds', 'Count']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Bounds', 'Count'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Bounds', 'Count']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Bounds', 'Count']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Bounds', 'Count'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Bounds', 'Count']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Bounds', 'Count']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Bounds', 'Count'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Bounds', 'Count']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Bounds', 'Count']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Bounds', 'Count'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Bounds', 'Count']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Bounds', 'Count']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Bounds', 'Count'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Bounds', 'Count']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Bounds', 'Count']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Bounds', 'Count'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Bounds', 'Count']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Bounds', 'Count']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Bounds', 'Count'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Bounds', 'Count']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Bounds', 'Count']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Bounds', 'Count'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Bounds', 'Count']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Bounds', 'Count']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Bounds', 'Count'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Bounds', 'Count']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Bounds', 'Count']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Bounds', 'Count'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Bounds', 'Count']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Bounds', 'Count']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Bounds', 'Count'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Bounds', 'Count']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Bounds', 'Count']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Bounds', 'Count'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Bounds', 'NumberOfPolygons', 'Count']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Bounds', 'NumberOfPolygons', 'Count']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Bounds', 'NumberOfPolygons', 'Count'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Bounds', 'NumberOfPolygons', 'Count']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Bounds', 'NumberOfPolygons', 'Count']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Bounds', 'NumberOfPolygons', 'Count'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Bounds', 'NumberOfPolylines', 'Count']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Bounds', 'NumberOfPolylines', 'Count']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Bounds', 'NumberOfPolylines', 'Count'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Bounds', 'NumberOfPolylines', 'Count']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Bounds', 'NumberOfPolylines', 'Count']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Bounds', 'NumberOfPolylines', 'Count'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '4b', '4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Bounds', 'iGraphicsMode', 'exScale', 'eyScale', 'cStrings']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Bounds', 'iGraphicsMode', 'exScale', 'eyScale', 'cStrings']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Bounds', 'iGraphicsMode', 'exScale', 'eyScale', 'cStrings'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '4b', '4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Bounds', 'iGraphicsMode', 'exScale', 'eyScale', 'cStrings']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Bounds', 'iGraphicsMode', 'exScale', 'eyScale', 'cStrings']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Bounds', 'iGraphicsMode', 'exScale', 'eyScale', 'cStrings'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Box']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Box']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Box'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '8b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Box', 'Corner']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Box', 'Corner']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Box', 'Corner'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '8b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Pixel', 'Color']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Pixel', 'Color']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Pixel', 'Color'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'x', 'y', 'cChars', 'fuOptions', 'iGraphicsMode', 'exScale', 'eyScale']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'x', 'y', 'cChars', 'fuOptions', 'iGraphicsMode', 'exScale', 'eyScale']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'x', 'y', 'cChars', 'fuOptions', 'iGraphicsMode', 'exScale', 'eyScale'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Bounds']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Bounds']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Bounds'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Bounds']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Bounds']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Bounds'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'cjIn']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'cjIn']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'cjIn'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'cjIn']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'cjIn']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'cjIn'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'cjDriver', 'cjIn']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'cjDriver', 'cjIn']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'cjDriver', 'cjIn'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b', '12b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'ihBrush', 'LogBrush']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'ihBrush', 'LogBrush']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'ihBrush', 'LogBrush'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'ihCS']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'ihCS']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'ihCS'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'ihCS', 'dwFlags', 'cbData']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'ihCS', 'dwFlags', 'cbData']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'ihCS', 'dwFlags', 'cbData'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'ihBrush', 'Usage', 'offBmi', 'cbBmi', 'offBits', 'cbBits']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'ihBrush', 'Usage', 'offBmi', 'cbBmi', 'offBits', 'cbBits']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'ihBrush', 'Usage', 'offBmi', 'cbBmi', 'offBits', 'cbBits'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'ihBrush', 'Usage', 'offBmi', 'cbBmi', 'offBits', 'cbBits']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'ihBrush', 'Usage', 'offBmi', 'cbBmi', 'offBits', 'cbBits']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'ihBrush', 'Usage', 'offBmi', 'cbBmi', 'offBits', 'cbBits'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'ihPal']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'ihPal']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'ihPal'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b', '16b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'ihPen', 'LogPen']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'ihPen', 'LogPen']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'ihPen', 'LogPen'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'ihFonts']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'ihFonts']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'ihFonts'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b', '4b', '4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'ihPen', 'offBmi', 'cbBmi', 'offBits', 'cbBits']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'ihPen', 'offBmi', 'cbBmi', 'offBits', 'cbBits']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'ihPen', 'offBmi', 'cbBmi', 'offBits', 'cbBits'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b', '4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'ihPalette', 'nFirstEntry', 'nPalEntries', 'nReserved']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'ihPalette', 'nFirstEntry', 'nPalEntries', 'nReserved']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'ihPalette', 'nFirstEntry', 'nPalEntries', 'nReserved'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'ihCS']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'ihCS']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'ihCS'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'ihObject']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'ihObject']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'ihObject'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'ihPal', 'NumberOfEntries']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'ihPal', 'NumberOfEntries']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'ihPal', 'NumberOfEntries'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'ihObject']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'ihObject']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'ihObject'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'ihPal']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'ihPal']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'ihPal'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'ihCS']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'ihCS']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'ihCS'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'ihPal', 'Start', 'NumberofEntries']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'ihPal', 'Start', 'NumberofEntries']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'ihPal', 'Start', 'NumberofEntries'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Bounds', 'cbData']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Bounds', 'cbData']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Bounds', 'cbData'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'cbData']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'cbData']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'cbData'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b', '4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'dwAction', 'dwFlags', 'cbName', 'cbData']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'dwAction', 'dwFlags', 'cbName', 'cbData']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'dwAction', 'dwFlags', 'cbName', 'cbData'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '8b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'ufi']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'ufi']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'ufi'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '16b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Bounds', 'RgnDataSize']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Bounds', 'RgnDataSize']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Bounds', 'RgnDataSize'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '8b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Offset']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Offset']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Offset'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '40b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'pfd']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'pfd']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'pfd'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'SavedDC']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'SavedDC']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'SavedDC'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b', '4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'xNum', 'xDenom', 'yNum', 'yDenom']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'xNum', 'xDenom', 'yNum', 'yDenom']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'xNum', 'xDenom', 'yNum', 'yDenom'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b', '4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'xNum', 'xDenom', 'yNum', 'yDenom']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'xNum', 'xDenom', 'yNum', 'yDenom']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'xNum', 'xDenom', 'yNum', 'yDenom'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'ArcDirection']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'ArcDirection']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'ArcDirection'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Color']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Color']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Color'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'BackgroundMode']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'BackgroundMode']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'BackgroundMode'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '8b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Origin']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Origin']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Origin'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '24b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'ColorAdjustment']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'ColorAdjustment']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'ColorAdjustment'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'ICMMode']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'ICMMode']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'ICMMode'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'dwFlags', 'cbName', 'cbData']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'dwFlags', 'cbName', 'cbData']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'dwFlags', 'cbName', 'cbData'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'dwFlags', 'cbName', 'cbData']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'dwFlags', 'cbName', 'cbData']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'dwFlags', 'cbName', 'cbData'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'LayoutMode']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'LayoutMode']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'LayoutMode'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b', '8b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'uNumLinkedUFI', 'Reserved']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'uNumLinkedUFI', 'Reserved']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'uNumLinkedUFI', 'Reserved'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'MapMode']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'MapMode']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'MapMode'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Flags']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Flags']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Flags'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'MiterLimit']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'MiterLimit']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'MiterLimit'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'PolygonFillMode']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'PolygonFillMode']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'PolygonFillMode'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'ROP2Mode']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'ROP2Mode']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'ROP2Mode'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'StretchMode']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'StretchMode']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'StretchMode'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'TextAlignmentMode']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'TextAlignmentMode']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'TextAlignmentMode'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Color']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Color']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Color'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '4b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'nBreakExtra', 'nBreakCount']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'nBreakExtra', 'nBreakCount']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'nBreakExtra', 'nBreakCount'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '8b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Extent']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Extent']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Extent'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '8b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Origin']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Origin']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Origin'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '8b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Extent']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Extent']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Extent'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '8b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Origin']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Origin']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Origin'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '24b', '4b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Xform', 'ModifyWorldTransformMode']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Xform', 'ModifyWorldTransformMode']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Xform', 'ModifyWorldTransformMode'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer

class ParsedHeader:
    format = ['4b', '4b', '24b']

    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        fields = ['Type', 'Size', 'Xform']
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255 
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        fields = ['Type', 'Size', 'Xform']
        parsed_fields = {field: getattr(self, field) for field in fields}
        return f"<ParsedHeader {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        fields = ['Type', 'Size', 'Xform'] # These are the fields of this object.
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



# This wasn't in the specific format which this script expects. Just add it here....


class EMR_SAVEDC:
    format = ["4b", "4b"]
    name = "EMR_SAVEDC"
    has_variable = False
    fields = ["Type", "Size"] # These are the fields of this object.
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        print("unpacked: ")
        print(unpacked)
        for field, value in zip(self.fields, unpacked):
            print("value == "+str(value))
            if isinstance(value, tuple): # This is a multibyte value.
                # Should be integers all
                # Convert to unsigned bytes...
                value = [to_unsigned(x) for x in value]
                assert all([x >= 0 and x <= 255 for x in value]) # Should be integers representing single bytes.
                # Make a list and then just use bytes
                b = bytes(value)
                # Now make the integer...
                # int.from_bytes(byte_data, byteorder='little')
                integer = int.from_bytes(b, byteorder='little')
                setattr(self, field, (len(b), integer))
            else:
                value = to_unsigned(value)
                assert value >= 0 and value <= 255
                setattr(self, field, (1, value)) # Size of one byte
        self.remaining_data = data[struct.calcsize("".join(self.format)):]
        print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_SAVEDC {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

    def serialize(self):
        out = b"" # Initialize empty bytes output
        for i, format_string in enumerate(self.format):
            # The corresponding field is fields[i]
            field_name = self.fields[i]
            field_val = getattr(self, field_name) # Get the actual value of the field from this object.
            field_length = field_val[0]
            field_integer = field_val[1]
            # Now try to unpack the integer into the format.
            # field_bytes = struct.pack(format_string, field_val)
            field_bytes = field_integer.to_bytes(field_length, byteorder='little') # num.to_bytes(4, byteorder='little')
            out += field_bytes # Add the actual value to the output
        return out # Return the output bytes



