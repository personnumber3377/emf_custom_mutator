import struct

def to_unsigned(byte_integer: int) -> int: # Converts a signed integer in a single byte to an unsigned integer.
    # assert byte_integer >= 0 and byte_integer <= 255
    assert byte_integer >= -128 and byte_integer <= 127
    if byte_integer < 0:
        byte_integer += 256
    return byte_integer


class EMR_ALPHABLEND:
    format = ['4b', '4b', '16b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '24b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b']
    name = "EMR_ALPHABLEND"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'xDest', 'yDest', 'cxDest', 'cyDest', 'BLENDFUNCTION', 'xSrc', 'ySrc', 'XformSrc', 'BkColorSrc', 'UsageSrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc', 'cxSrc', 'cySrc'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_ALPHABLEND {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_BITBLT:
    format = ['4b', '4b', '16b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '24b', '4b', '4b', '4b', '4b', '4b', '4b']
    name = "EMR_BITBLT"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'xDest', 'yDest', 'cxDest', 'cyDest', 'BitBltRasterOperation', 'xSrc', 'ySrc', 'XformSrc', 'BkColorSrc', 'UsageSrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_BITBLT {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_MASKBLT:
    format = ['4b', '4b', '16b', '4b', '4b', '4b', '4b', '4b', '2b', '4b', '4b', '24b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b']
    name = "EMR_MASKBLT"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'xDest', 'yDest', 'cxDest', 'cyDest', 'ROP4', 'Reserved', 'xSrc', 'ySrc', 'XformSrc', 'BkColorSrc', 'UsageSrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc', 'xMask', 'yMask', 'UsageMask', 'offBmiMask', 'cbBmiMask', 'offBitsMask', 'cbBitsMask'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_MASKBLT {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_PLGBLT:
    format = ['4b', '4b', '16b', '24b', '4b', '4b', '4b', '4b', '24b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b']
    name = "EMR_PLGBLT"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'aptlDest', 'xSrc', 'ySrc', 'cxSrc', 'cySrc', 'XformSrc', 'BkColorSrc', 'UsageSrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc', 'xMask', 'yMask', 'UsageMask', 'offBmiMask', 'cbBmiMask', 'offBitsMask', 'cbBitsMask'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_PLGBLT {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_SETDIBITSTODEVICE:
    format = ['4b', '4b', '16b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b']
    name = "EMR_SETDIBITSTODEVICE"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'xDest', 'yDest', 'xSrc', 'ySrc', 'cxSrc', 'cySrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc', 'UsageSrc', 'iStartScan', 'cScans'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_SETDIBITSTODEVICE {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_STRETCHBLT:
    format = ['4b', '4b', '16b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '24b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b']
    name = "EMR_STRETCHBLT"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'xDest', 'yDest', 'cxDest', 'cyDest', 'BitBltRasterOperation', 'xSrc', 'ySrc', 'XformSrc', 'BkColorSrc', 'UsageSrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc', 'cxSrc', 'cySrc'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_STRETCHBLT {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_STRETCHDIBITS:
    format = ['4b', '4b', '16b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b']
    name = "EMR_STRETCHDIBITS"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'xDest', 'yDest', 'xSrc', 'ySrc', 'cxSrc', 'cySrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc', 'UsageSrc', 'BitBltRasterOperation', 'cxDest', 'cyDest'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_STRETCHDIBITS {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_TRANSPARENTBLT:
    format = ['4b', '4b', '16b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '24b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b']
    name = "EMR_TRANSPARENTBLT"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'xDest', 'yDest', 'cxDest', 'cyDest', 'TransparentColor', 'xSrc', 'ySrc', 'XformSrc', 'BkColorSrc', 'UsageSrc', 'offBmiSrc', 'cbBmiSrc', 'offBitsSrc', 'cbBitsSrc', 'cxSrc', 'cySrc'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_TRANSPARENTBLT {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_EXCLUDECLIPRECT:
    format = ['4b', '4b', '16b']
    name = "EMR_EXCLUDECLIPRECT"
    has_variable = False
    fields = ['Type', 'Size', 'Clip'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_EXCLUDECLIPRECT {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_EXTSELECTCLIPRGN:
    format = ['4b', '4b', '4b', '4b']
    name = "EMR_EXTSELECTCLIPRGN"
    has_variable = True
    fields = ['Type', 'Size', 'RgnDataSize', 'RegionMode'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_EXTSELECTCLIPRGN {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_INTERSECTCLIPRECT:
    format = ['4b', '4b', '16b']
    name = "EMR_INTERSECTCLIPRECT"
    has_variable = False
    fields = ['Type', 'Size', 'Clip'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_INTERSECTCLIPRECT {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_OFFSETCLIPRGN:
    format = ['4b', '4b', '8b']
    name = "EMR_OFFSETCLIPRGN"
    has_variable = False
    fields = ['Type', 'Size', 'Offset'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_OFFSETCLIPRGN {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_SELECTCLIPPATH:
    format = ['4b', '4b', '4b']
    name = "EMR_SELECTCLIPPATH"
    has_variable = True
    fields = ['Type', 'Size', 'RegionMode'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_SELECTCLIPPATH {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_COMMENT:
    format = ['4b', '4b']
    name = "EMR_COMMENT"
    has_variable = True
    fields = ['Type', 'Size'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_COMMENT {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_COMMENT_EMFPLUS:
    format = ['4b', '4b', '4b']
    name = "EMR_COMMENT_EMFPLUS"
    has_variable = True
    fields = ['Type', 'Size', 'CommentIdentifier'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_COMMENT_EMFPLUS {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_COMMENT_EMFSPOOL:
    format = ['4b', '4b', '4b', '4b']
    name = "EMR_COMMENT_EMFSPOOL"
    has_variable = True
    fields = ['Type', 'Size', 'CommentIdentifier', 'EMFSpoolRecordIdentifier'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_COMMENT_EMFSPOOL {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_EOF:
    format = ['4b', '4b', '4b', '4b', '4b']
    name = "EMR_EOF"
    has_variable = True
    fields = ['Type', 'Size', 'nPalEntries', 'offPalEntries', 'SizeLast'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_EOF {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_ANGLEARC:
    format = ['4b', '4b', '8b', '4b', '4b', '4b']
    name = "EMR_ANGLEARC"
    has_variable = False
    fields = ['Type', 'Size', 'Center', 'Radius', 'StartAngle', 'SweepAngle'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_ANGLEARC {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_ARC:
    format = ['4b', '4b', '16b', '8b', '8b']
    name = "EMR_ARC"
    has_variable = False
    fields = ['Type', 'Size', 'Box', 'Start', 'End'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_ARC {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_ARCTO:
    format = ['4b', '4b', '16b', '8b', '8b']
    name = "EMR_ARCTO"
    has_variable = False
    fields = ['Type', 'Size', 'Box', 'Start', 'End'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_ARCTO {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_CHORD:
    format = ['4b', '4b', '16b', '8b', '8b']
    name = "EMR_CHORD"
    has_variable = False
    fields = ['Type', 'Size', 'Box', 'Start', 'End'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_CHORD {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_ELLIPSE:
    format = ['4b', '4b', '16b']
    name = "EMR_ELLIPSE"
    has_variable = False
    fields = ['Type', 'Size', 'Box'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_ELLIPSE {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_EXTFLOODFILL:
    format = ['4b', '4b', '8b', '4b', '4b']
    name = "EMR_EXTFLOODFILL"
    has_variable = False
    fields = ['Type', 'Size', 'Start', 'Color', 'FloodFillMode'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_EXTFLOODFILL {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_EXTTEXTOUTA:
    format = ['4b', '4b', '16b', '4b', '4b', '4b']
    name = "EMR_EXTTEXTOUTA"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'iGraphicsMode', 'exScale', 'eyScale'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_EXTTEXTOUTA {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_EXTTEXTOUTW:
    format = ['4b', '4b', '16b', '4b', '4b', '4b']
    name = "EMR_EXTTEXTOUTW"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'iGraphicsMode', 'exScale', 'eyScale'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_EXTTEXTOUTW {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_FILLPATH:
    format = ['4b', '4b', '16b']
    name = "EMR_FILLPATH"
    has_variable = False
    fields = ['Type', 'Size', 'Bounds'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_FILLPATH {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_FILLRGN:
    format = ['4b', '4b', '16b', '4b', '4b']
    name = "EMR_FILLRGN"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'RgnDataSize', 'ihBrush'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_FILLRGN {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_FRAMERGN:
    format = ['4b', '4b', '16b', '4b', '4b', '4b', '4b']
    name = "EMR_FRAMERGN"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'RgnDataSize', 'ihBrush', 'Width', 'Height'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_FRAMERGN {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_GRADIENTFILL:
    format = ['4b', '4b', '16b', '4b', '4b', '4b']
    name = "EMR_GRADIENTFILL"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'nVer', 'nTri', 'ulMode'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_GRADIENTFILL {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_LINETO:
    format = ['4b', '4b', '8b']
    name = "EMR_LINETO"
    has_variable = False
    fields = ['Type', 'Size', 'Point'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_LINETO {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_PAINTRGN:
    format = ['4b', '4b', '16b', '4b']
    name = "EMR_PAINTRGN"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'RgnDataSize'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_PAINTRGN {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_PIE:
    format = ['4b', '4b', '16b', '8b', '8b']
    name = "EMR_PIE"
    has_variable = False
    fields = ['Type', 'Size', 'Box', 'Start', 'End'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_PIE {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_POLYBEZIER:
    format = ['4b', '4b', '16b', '4b']
    name = "EMR_POLYBEZIER"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'Count'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_POLYBEZIER {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_POLYBEZIER16:
    format = ['4b', '4b', '16b', '4b']
    name = "EMR_POLYBEZIER16"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'Count'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_POLYBEZIER16 {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_POLYBEZIERTO:
    format = ['4b', '4b', '16b', '4b']
    name = "EMR_POLYBEZIERTO"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'Count'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_POLYBEZIERTO {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_POLYBEZIERTO16:
    format = ['4b', '4b', '16b', '4b']
    name = "EMR_POLYBEZIERTO16"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'Count'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_POLYBEZIERTO16 {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_POLYDRAW:
    format = ['4b', '4b', '16b', '4b']
    name = "EMR_POLYDRAW"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'Count'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_POLYDRAW {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_POLYDRAW16:
    format = ['4b', '4b', '16b', '4b']
    name = "EMR_POLYDRAW16"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'Count'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_POLYDRAW16 {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_POLYGON:
    format = ['4b', '4b', '16b', '4b']
    name = "EMR_POLYGON"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'Count'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_POLYGON {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_POLYGON16:
    format = ['4b', '4b', '16b', '4b']
    name = "EMR_POLYGON16"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'Count'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_POLYGON16 {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_POLYLINE:
    format = ['4b', '4b', '16b', '4b']
    name = "EMR_POLYLINE"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'Count'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_POLYLINE {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_POLYLINE16:
    format = ['4b', '4b', '16b', '4b']
    name = "EMR_POLYLINE16"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'Count'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_POLYLINE16 {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_POLYLINETO:
    format = ['4b', '4b', '16b', '4b']
    name = "EMR_POLYLINETO"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'Count'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_POLYLINETO {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_POLYLINETO16:
    format = ['4b', '4b', '16b', '4b']
    name = "EMR_POLYLINETO16"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'Count'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_POLYLINETO16 {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_POLYPOLYGON:
    format = ['4b', '4b', '16b', '4b', '4b']
    name = "EMR_POLYPOLYGON"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'NumberOfPolygons', 'Count'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_POLYPOLYGON {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_POLYPOLYGON16:
    format = ['4b', '4b', '16b', '4b', '4b']
    name = "EMR_POLYPOLYGON16"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'NumberOfPolygons', 'Count'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_POLYPOLYGON16 {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_POLYPOLYLINE:
    format = ['4b', '4b', '16b', '4b', '4b']
    name = "EMR_POLYPOLYLINE"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'NumberOfPolylines', 'Count'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_POLYPOLYLINE {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_POLYPOLYLINE16:
    format = ['4b', '4b', '16b', '4b', '4b']
    name = "EMR_POLYPOLYLINE16"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'NumberOfPolylines', 'Count'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_POLYPOLYLINE16 {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_POLYTEXTOUTA:
    format = ['4b', '4b', '16b', '4b', '4b', '4b', '4b']
    name = "EMR_POLYTEXTOUTA"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'iGraphicsMode', 'exScale', 'eyScale', 'cStrings'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_POLYTEXTOUTA {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_POLYTEXTOUTW:
    format = ['4b', '4b', '16b', '4b', '4b', '4b', '4b']
    name = "EMR_POLYTEXTOUTW"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'iGraphicsMode', 'exScale', 'eyScale', 'cStrings'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_POLYTEXTOUTW {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_RECTANGLE:
    format = ['4b', '4b', '16b']
    name = "EMR_RECTANGLE"
    has_variable = False
    fields = ['Type', 'Size', 'Box'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_RECTANGLE {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_ROUNDRECT:
    format = ['4b', '4b', '16b', '8b']
    name = "EMR_ROUNDRECT"
    has_variable = False
    fields = ['Type', 'Size', 'Box', 'Corner'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_ROUNDRECT {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_SETPIXELV:
    format = ['4b', '4b', '8b', '4b']
    name = "EMR_SETPIXELV"
    has_variable = False
    fields = ['Type', 'Size', 'Pixel', 'Color'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_SETPIXELV {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_SMALLTEXTOUT:
    format = ['4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b']
    name = "EMR_SMALLTEXTOUT"
    has_variable = True
    fields = ['Type', 'Size', 'x', 'y', 'cChars', 'fuOptions', 'iGraphicsMode', 'exScale', 'eyScale'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_SMALLTEXTOUT {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_STROKEANDFILLPATH:
    format = ['4b', '4b', '16b']
    name = "EMR_STROKEANDFILLPATH"
    has_variable = False
    fields = ['Type', 'Size', 'Bounds'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_STROKEANDFILLPATH {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_STROKEPATH:
    format = ['4b', '4b', '16b']
    name = "EMR_STROKEPATH"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_STROKEPATH {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_DRAWESCAPE:
    format = ['4b', '4b', '4b']
    name = "EMR_DRAWESCAPE"
    has_variable = True
    fields = ['Type', 'Size', 'cjIn'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_DRAWESCAPE {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_EXTESCAPE:
    format = ['4b', '4b', '4b']
    name = "EMR_EXTESCAPE"
    has_variable = True
    fields = ['Type', 'Size', 'cjIn'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_EXTESCAPE {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_NAMEDESCAPE:
    format = ['4b', '4b', '4b', '4b']
    name = "EMR_NAMEDESCAPE"
    has_variable = True
    fields = ['Type', 'Size', 'cjDriver', 'cjIn'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_NAMEDESCAPE {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_CREATEBRUSHINDIRECT:
    format = ['4b', '4b', '4b', '12b']
    name = "EMR_CREATEBRUSHINDIRECT"
    has_variable = False
    fields = ['Type', 'Size', 'ihBrush', 'LogBrush'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_CREATEBRUSHINDIRECT {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_CREATECOLORSPACE:
    format = ['4b', '4b', '4b']
    name = "EMR_CREATECOLORSPACE"
    has_variable = True
    fields = ['Type', 'Size', 'ihCS'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_CREATECOLORSPACE {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_CREATECOLORSPACEW:
    format = ['4b', '4b', '4b', '4b', '4b']
    name = "EMR_CREATECOLORSPACEW"
    has_variable = True
    fields = ['Type', 'Size', 'ihCS', 'dwFlags', 'cbData'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_CREATECOLORSPACEW {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_CREATEDIBPATTERNBRUSHPT:
    format = ['4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b']
    name = "EMR_CREATEDIBPATTERNBRUSHPT"
    has_variable = True
    fields = ['Type', 'Size', 'ihBrush', 'Usage', 'offBmi', 'cbBmi', 'offBits', 'cbBits'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_CREATEDIBPATTERNBRUSHPT {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_CREATEMONOBRUSH:
    format = ['4b', '4b', '4b', '4b', '4b', '4b', '4b', '4b']
    name = "EMR_CREATEMONOBRUSH"
    has_variable = True
    fields = ['Type', 'Size', 'ihBrush', 'Usage', 'offBmi', 'cbBmi', 'offBits', 'cbBits'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_CREATEMONOBRUSH {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_CREATEPALETTE:
    format = ['4b', '4b', '4b']
    name = "EMR_CREATEPALETTE"
    has_variable = True
    fields = ['Type', 'Size', 'ihPal'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_CREATEPALETTE {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_CREATEPEN:
    format = ['4b', '4b', '4b', '16b']
    name = "EMR_CREATEPEN"
    has_variable = False
    fields = ['Type', 'Size', 'ihPen', 'LogPen'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_CREATEPEN {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_EXTCREATEFONTINDIRECTW:
    format = ['4b', '4b', '4b']
    name = "EMR_EXTCREATEFONTINDIRECTW"
    has_variable = True
    fields = ['Type', 'Size', 'ihFonts'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_EXTCREATEFONTINDIRECTW {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_EXTCREATEPEN:
    format = ['4b', '4b', '4b', '4b', '4b', '4b', '4b']
    name = "EMR_EXTCREATEPEN"
    has_variable = True
    fields = ['Type', 'Size', 'ihPen', 'offBmi', 'cbBmi', 'offBits', 'cbBits'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_EXTCREATEPEN {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_COLORCORRECTPALETTE:
    format = ['4b', '4b', '4b', '4b', '4b', '4b']
    name = "EMR_COLORCORRECTPALETTE"
    has_variable = False
    fields = ['Type', 'Size', 'ihPalette', 'nFirstEntry', 'nPalEntries', 'nReserved'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_COLORCORRECTPALETTE {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_DELETECOLORSPACE:
    format = ['4b', '4b', '4b']
    name = "EMR_DELETECOLORSPACE"
    has_variable = False
    fields = ['Type', 'Size', 'ihCS'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_DELETECOLORSPACE {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_DELETEOBJECT:
    format = ['4b', '4b', '4b']
    name = "EMR_DELETEOBJECT"
    has_variable = False
    fields = ['Type', 'Size', 'ihObject'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_DELETEOBJECT {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_RESIZEPALETTE:
    format = ['4b', '4b', '4b', '4b']
    name = "EMR_RESIZEPALETTE"
    has_variable = False
    fields = ['Type', 'Size', 'ihPal', 'NumberOfEntries'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_RESIZEPALETTE {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_SELECTOBJECT:
    format = ['4b', '4b', '4b']
    name = "EMR_SELECTOBJECT"
    has_variable = False
    fields = ['Type', 'Size', 'ihObject'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_SELECTOBJECT {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_SELECTPALETTE:
    format = ['4b', '4b', '4b']
    name = "EMR_SELECTPALETTE"
    has_variable = False
    fields = ['Type', 'Size', 'ihPal'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_SELECTPALETTE {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_SETCOLORSPACE:
    format = ['4b', '4b', '4b']
    name = "EMR_SETCOLORSPACE"
    has_variable = False
    fields = ['Type', 'Size', 'ihCS'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_SETCOLORSPACE {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_SETPALETTEENTRIES:
    format = ['4b', '4b', '4b', '4b', '4b']
    name = "EMR_SETPALETTEENTRIES"
    has_variable = True
    fields = ['Type', 'Size', 'ihPal', 'Start', 'NumberofEntries'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_SETPALETTEENTRIES {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_GLSBOUNDEDRECORD:
    format = ['4b', '4b', '16b', '4b']
    name = "EMR_GLSBOUNDEDRECORD"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'cbData'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_GLSBOUNDEDRECORD {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_GLSRECORD:
    format = ['4b', '4b', '4b']
    name = "EMR_GLSRECORD"
    has_variable = True
    fields = ['Type', 'Size', 'cbData'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_GLSRECORD {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_COLORMATCHTOTARGETW:
    format = ['4b', '4b', '4b', '4b', '4b', '4b']
    name = "EMR_COLORMATCHTOTARGETW"
    has_variable = True
    fields = ['Type', 'Size', 'dwAction', 'dwFlags', 'cbName', 'cbData'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_COLORMATCHTOTARGETW {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_FORCEUFIMAPPING:
    format = ['4b', '4b', '8b']
    name = "EMR_FORCEUFIMAPPING"
    has_variable = False
    fields = ['Type', 'Size', 'ufi'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_FORCEUFIMAPPING {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_INVERTRGN:
    format = ['4b', '4b', '16b', '4b']
    name = "EMR_INVERTRGN"
    has_variable = True
    fields = ['Type', 'Size', 'Bounds', 'RgnDataSize'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_INVERTRGN {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_MOVETOEX:
    format = ['4b', '4b', '8b']
    name = "EMR_MOVETOEX"
    has_variable = False
    fields = ['Type', 'Size', 'Offset'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_MOVETOEX {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_PIXELFORMAT:
    format = ['4b', '4b', '40b']
    name = "EMR_PIXELFORMAT"
    has_variable = False
    fields = ['Type', 'Size', 'pfd'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_PIXELFORMAT {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_RESTOREDC:
    format = ['4b', '4b', '4b']
    name = "EMR_RESTOREDC"
    has_variable = False
    fields = ['Type', 'Size', 'SavedDC'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_RESTOREDC {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_SCALEVIEWPORTEXTEX:
    format = ['4b', '4b', '4b', '4b', '4b', '4b']
    name = "EMR_SCALEVIEWPORTEXTEX"
    has_variable = False
    fields = ['Type', 'Size', 'xNum', 'xDenom', 'yNum', 'yDenom'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_SCALEVIEWPORTEXTEX {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_SCALEWINDOWEXTEX:
    format = ['4b', '4b', '4b', '4b', '4b', '4b']
    name = "EMR_SCALEWINDOWEXTEX"
    has_variable = False
    fields = ['Type', 'Size', 'xNum', 'xDenom', 'yNum', 'yDenom'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_SCALEWINDOWEXTEX {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_SETARCDIRECTION:
    format = ['4b', '4b', '4b']
    name = "EMR_SETARCDIRECTION"
    has_variable = False
    fields = ['Type', 'Size', 'ArcDirection'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_SETARCDIRECTION {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_SETBKCOLOR:
    format = ['4b', '4b', '4b']
    name = "EMR_SETBKCOLOR"
    has_variable = False
    fields = ['Type', 'Size', 'Color'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_SETBKCOLOR {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_SETBKMODE:
    format = ['4b', '4b', '4b']
    name = "EMR_SETBKMODE"
    has_variable = False
    fields = ['Type', 'Size', 'BackgroundMode'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_SETBKMODE {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_SETBRUSHORGEX:
    format = ['4b', '4b', '8b']
    name = "EMR_SETBRUSHORGEX"
    has_variable = False
    fields = ['Type', 'Size', 'Origin'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_SETBRUSHORGEX {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_SETCOLORADJUSTMENT:
    format = ['4b', '4b', '24b']
    name = "EMR_SETCOLORADJUSTMENT"
    has_variable = False
    fields = ['Type', 'Size', 'ColorAdjustment'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_SETCOLORADJUSTMENT {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_SETICMMODE:
    format = ['4b', '4b', '4b']
    name = "EMR_SETICMMODE"
    has_variable = False
    fields = ['Type', 'Size', 'ICMMode'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_SETICMMODE {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_SETICMPROFILEA:
    format = ['4b', '4b', '4b', '4b', '4b']
    name = "EMR_SETICMPROFILEA"
    has_variable = True
    fields = ['Type', 'Size', 'dwFlags', 'cbName', 'cbData'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_SETICMPROFILEA {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_SETICMPROFILEW:
    format = ['4b', '4b', '4b', '4b', '4b']
    name = "EMR_SETICMPROFILEW"
    has_variable = True
    fields = ['Type', 'Size', 'dwFlags', 'cbName', 'cbData'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_SETICMPROFILEW {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_SETLAYOUT:
    format = ['4b', '4b', '4b']
    name = "EMR_SETLAYOUT"
    has_variable = False
    fields = ['Type', 'Size', 'LayoutMode'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_SETLAYOUT {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_SETLINKEDUFIS:
    format = ['4b', '4b', '4b', '8b']
    name = "EMR_SETLINKEDUFIS"
    has_variable = True
    fields = ['Type', 'Size', 'uNumLinkedUFI', 'Reserved'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_SETLINKEDUFIS {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_SETMAPMODE:
    format = ['4b', '4b', '4b']
    name = "EMR_SETMAPMODE"
    has_variable = False
    fields = ['Type', 'Size', 'MapMode'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_SETMAPMODE {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_SETMAPPERFLAGS:
    format = ['4b', '4b', '4b']
    name = "EMR_SETMAPPERFLAGS"
    has_variable = False
    fields = ['Type', 'Size', 'Flags'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_SETMAPPERFLAGS {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_SETMITERLIMIT:
    format = ['4b', '4b', '4b']
    name = "EMR_SETMITERLIMIT"
    has_variable = False
    fields = ['Type', 'Size', 'MiterLimit'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_SETMITERLIMIT {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_SETPOLYFILLMODE:
    format = ['4b', '4b', '4b']
    name = "EMR_SETPOLYFILLMODE"
    has_variable = False
    fields = ['Type', 'Size', 'PolygonFillMode'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_SETPOLYFILLMODE {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_SETROP2:
    format = ['4b', '4b', '4b']
    name = "EMR_SETROP2"
    has_variable = False
    fields = ['Type', 'Size', 'ROP2Mode'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_SETROP2 {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_SETSTRETCHBLTMODE:
    format = ['4b', '4b', '4b']
    name = "EMR_SETSTRETCHBLTMODE"
    has_variable = False
    fields = ['Type', 'Size', 'StretchMode'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_SETSTRETCHBLTMODE {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_SETTEXTALIGN:
    format = ['4b', '4b', '4b']
    name = "EMR_SETTEXTALIGN"
    has_variable = False
    fields = ['Type', 'Size', 'TextAlignmentMode'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_SETTEXTALIGN {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_SETTEXTCOLOR:
    format = ['4b', '4b', '4b']
    name = "EMR_SETTEXTCOLOR"
    has_variable = False
    fields = ['Type', 'Size', 'Color'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_SETTEXTCOLOR {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_SETTEXTJUSTIFICATION:
    format = ['4b', '4b', '4b', '4b']
    name = "EMR_SETTEXTJUSTIFICATION"
    has_variable = False
    fields = ['Type', 'Size', 'nBreakExtra', 'nBreakCount'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_SETTEXTJUSTIFICATION {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_SETVIEWPORTEXTEX:
    format = ['4b', '4b', '8b']
    name = "EMR_SETVIEWPORTEXTEX"
    has_variable = False
    fields = ['Type', 'Size', 'Extent'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_SETVIEWPORTEXTEX {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_SETVIEWPORTORGEX:
    format = ['4b', '4b', '8b']
    name = "EMR_SETVIEWPORTORGEX"
    has_variable = False
    fields = ['Type', 'Size', 'Origin'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_SETVIEWPORTORGEX {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_SETWINDOWEXTEX:
    format = ['4b', '4b', '8b']
    name = "EMR_SETWINDOWEXTEX"
    has_variable = False
    fields = ['Type', 'Size', 'Extent'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_SETWINDOWEXTEX {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_SETWINDOWORGEX:
    format = ['4b', '4b', '8b']
    name = "EMR_SETWINDOWORGEX"
    has_variable = False
    fields = ['Type', 'Size', 'Origin'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_SETWINDOWORGEX {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_MODIFYWORLDTRANSFORM:
    format = ['4b', '4b', '24b', '4b']
    name = "EMR_MODIFYWORLDTRANSFORM"
    has_variable = False
    fields = ['Type', 'Size', 'Xform', 'ModifyWorldTransformMode'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_MODIFYWORLDTRANSFORM {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
        return out # Return the output bytes





class EMR_SETWORLDTRANSFORM:
    format = ['4b', '4b', '24b']
    name = "EMR_SETWORLDTRANSFORM"
    has_variable = False
    fields = ['Type', 'Size', 'Xform'] # These are the fields of this object.
    variable_data = None
    def __init__(self, data):
        unpacked = []
        for f in self.format:
            unpacked.append(struct.unpack(f, data[:struct.calcsize(f)]))
            data = data[struct.calcsize(f):]
        #print("unpacked: ")
        #print(unpacked)
        for field, value in zip(self.fields, unpacked):
            #print("value == "+str(value))
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
        self.remaining_data = data # data[struct.calcsize("".join(self.format)):] # We do not need to do this here because we did this earlier.
        #print("Here is the size thing: "+str(struct.calcsize("".join(self.format))))
        # return self.remaining_data # Return the remaining data after reading the header.
        # Sanity checking. If the record doesn't have variable fields, then all of the data should be consumed. Otherwise this is an error condition.
        #print("Here is self.name: "+str(self.name))
        #print("Here is self.has_variable: "+str(self.has_variable))
        #print("Here is self.remaining_data: "+str(self.remaining_data))
        if not self.has_variable and self.remaining_data: # There is left over data even though record should not be variable.
            assert False
        if self.has_variable:
            # Set the variable data.
            self.variable_data = self.remaining_data # The variable data should be the data at the end. This actually may be b"" for optional fields...

    def mutable_fields(self) -> list:
        # This method returns the fields which do NOT contain the type or size fields.
        assert "Type" in self.fields
        assert "Size" in self.fields
        o = self.fields # Now try to do the thing.
        o.remove("Type")
        o.remove("Size")
        assert "Type" not in self.fields
        assert "Size" not in self.fields
        return 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            return cls(data)

    def __repr__(self):
        parsed_fields = {field: getattr(self, field) for field in self.fields}
        return f"<EMR_SETWORLDTRANSFORM {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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
        #if self.variable_data:
        #    print("Length of variable data: "+str(len(self.variable_data)))
        #    print("Variable data: "+str(self.variable_data))
        if self.has_variable:
            # Add variable data to the end.
            out += self.variable_data
        # Sanity checking. The "Size" field should actually match the size upon serialization. If not, then the mutator did not take care of the size correctly and there is a bug in the mutator.
        assert self.Size[1] == len(out)
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
        for field, value in zip(self.fields, unpacked):
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
        # self.remaining_data = data[struct.calcsize("".join(self.format)):]
        self.remaining_data = data

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



