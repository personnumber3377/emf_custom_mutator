import re

def gen_python_code(struct_format, fields):
    fh = open("template.py", "r")
    data = fh.read()
    fh.close()
    # 
    # STRUCT_FORMAT is struct_format and FIELDS is fields in the template.
    data = data.replace("STRUCT_FORMAT", struct_format)
    data = data.replace("FIELDS", fields)
    return data

def c_header_to_python(header):
    # Mapping of C types to struct format characters
    type_mapping = {
        # Integer types
        "BYTE": "1b",         # Unsigned 1 byte
        "CHAR": "1b",         # Signed 1 byte
        "UCHAR": "1b",        # Unsigned 1 byte
        "SHORT": "2b",        # Signed 2 bytes
        "USHORT": "2b",       # Unsigned 2 bytes
        "WORD": "2b",         # Unsigned 2 bytes (Windows-specific)
        "INT": "4b",          # Signed 4 bytes
        "UINT": "4b",         # Unsigned 4 bytes
        "LONG": "4b",         # Signed 4 bytes
        "ULONG": "4b",        # Unsigned 4 bytes
        "DWORD": "4b",        # Unsigned 4 bytes (Windows-specific)
        "LONGLONG": "8b",     # Signed 8 bytes
        "ULONGLONG": "8b",    # Unsigned 8 bytes
        "SIZE_T": "8b",       # Platform-dependent size type (64-bit here)

        # Floating-point types
        "FLOAT": "4b",        # 4 bytes
        "DOUBLE": "8b",       # 8 bytes

        # Character types
        "TCHAR": "1b",        # 1 character (use Unicode-specific mappings if needed)
        "WCHAR": "2b",        # 2 bytes (Unicode character)
        "CHAR16": "2b",       # UTF-16 2-byte character
        "CHAR32": "4b",       # UTF-32 4-byte character

        # Composite types
        "RECTL": "16b",       # Rectangle (4 signed LONGs, 4 bytes each = 16 bytes)
        "SIZEL": "8b",        # Size (2 signed LONGs, 4 bytes each = 8 bytes)
        "POINTL": "8b",       # Point (2 signed LONGs, 4 bytes each = 8 bytes)
        "RECT": "16b",        # Rectangle structure (4 signed LONGs = 16 bytes)
        "SIZE": "8b",         # Size structure (2 signed LONGs = 8 bytes)
        "POINT": "8b",        # Point structure (2 signed LONGs = 8 bytes)

        # Boolean types
        "BOOL": "4b",         # 4 bytes (commonly used in Windows)
        "BOOLEAN": "1b",      # 1 byte (commonly used in Unix)

        # Special types
        "HANDLE": "8b",       # Pointer to a handle (platform-dependent size, 64-bit assumed)
        "LPVOID": "8b",       # Void pointer (platform-dependent size, 64-bit assumed)
        "LPSTR": "8b",        # Pointer to a string
        "LPCSTR": "8b",       # Pointer to a constant string
        "LPWSTR": "8b",       # Pointer to a wide string
        "LPCWSTR": "8b",      # Pointer to a constant wide string

        # Unix-specific
        "int8_t": "1b",       # Signed 1 byte
        "uint8_t": "1b",      # Unsigned 1 byte
        "int16_t": "2b",      # Signed 2 bytes
        "uint16_t": "2b",     # Unsigned 2 bytes
        "int32_t": "4b",      # Signed 4 bytes
        "uint32_t": "4b",     # Unsigned 4 bytes
        "int64_t": "8b",      # Signed 8 bytes
        "uint64_t": "8b",     # Unsigned 8 bytes
        "pid_t": "4b",        # Process ID type (usually 4 bytes)
        "off_t": "8b",        # File offset type (usually 8 bytes)
        "time_t": "8b",       # Time type (signed 8 bytes)
        "ssize_t": "8b",      # Signed size type (usually 8 bytes)
        "size_t": "8b",       # Unsigned size type (usually 8 bytes)
        "uid_t": "4b",        # User ID (usually 4 bytes)
        "gid_t": "4b",        # Group ID (usually 4 bytes)

        # Pointers
        "void*": "8b",        # Generic pointer (platform-dependent size, 64-bit assumed)
        "char*": "8b",        # Pointer to a character array
        "int*": "8b",         # Pointer to an integer
        "float*": "8b",       # Pointer to a float
        "double*": "8b",      # Pointer to a double
    }

    # Regular expression to match C-style fields
    field_regex = re.compile(r"(\w+)\s+(\w+);")
    struct_format = [] # ""
    fields = []

    # Process the header line by line
    for line in header.splitlines():
        match = field_regex.search(line)
        if match:
            c_type, field_name = match.groups()
            if c_type in type_mapping:
                # struct_format += type_mapping[c_type]
                struct_format.append(type_mapping[c_type])
                fields.append(field_name)
            else:
                raise ValueError(f"Unknown type: {c_type}")

    # Generate Python code
    '''
    python_code = f"""import struct

class EMFHeader:
    format = '{struct_format}'

    def __init__(self, data):
        unpacked = struct.unpack(self.format, data)
        fields = {fields}
        for field, value in zip(fields, unpacked):
            setattr(self, field, value)

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as f:
            data = f.read(struct.calcsize(cls.format))
            return cls(data)
"""
    '''

    python_code = gen_python_code(str(struct_format), str(fields))
    return python_code

'''
# Example usage
c_header = """
DWORD   iType;
DWORD   nSize;
RECTL   rclBounds;
RECTL   rclFrame;
DWORD   dSignature;
DWORD   nVersion;
DWORD   nBytes;
DWORD   nRecords;
WORD    nHandles;
WORD    sReserved;
DWORD   nDescription;
DWORD   offDescription;
DWORD   nPalEntries;
SIZEL   szlDevice;
SIZEL   szlMillimeters;
"""
'''
#generated_code = c_header_to_python(c_header)
#print(generated_code)


def gen_header(filename: str) -> None:
    fh = open(filename, "r")
    data = fh.read()
    fh.close()
    print(c_header_to_python(data))
    return

import sys

if __name__=="__main__":
    if len(sys.argv) != 2:
        print("Usage: "+str(sys.argv[0])+" INPUT_C_HEADER_FILE")
        exit(0)
    gen_header(sys.argv[1])
    exit(0)