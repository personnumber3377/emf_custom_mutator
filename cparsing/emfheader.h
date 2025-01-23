typedef struct tagENHMETAHEADER {
    DWORD   iType;              // Record type
    DWORD   nSize;              // Size of this record in bytes
    RECTL   rclBounds;          // Bounds in device units (4 DWORDs)
    RECTL   rclFrame;           // Frame in .01 millimeter units (4 DWORDs)
    DWORD   dSignature;         // Signature
    DWORD   nVersion;           // Version of the metafile
    DWORD   nBytes;             // Total size of the metafile in bytes
    DWORD   nRecords;           // Number of records in the metafile
    WORD    nHandles;           // Number of handles in the handle table
    WORD    sReserved;          // Reserved, must be 0
    DWORD   nDescription;       // Number of characters in the description string
    DWORD   offDescription;     // Offset to the description string
    DWORD   nPalEntries;        // Number of palette entries
    SIZEL   szlDevice;          // Device resolution in pixels (2 DWORDs)
    SIZEL   szlMillimeters;     // Device resolution in millimeters (2 DWORDs)
} ENHMETAHEADER;