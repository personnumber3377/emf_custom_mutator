class NAME:
    format = STRUCT_FORMAT
    name = "NAME"
    has_variable = HAS_VARIABLE
    fields = FIELDS # These are the fields of this object.
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
        return f"<NAME {parsed_fields}, Remaining: {len(self.remaining_data)} bytes>"

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


