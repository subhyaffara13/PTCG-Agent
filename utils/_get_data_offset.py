
def _get_data_offset(zf: zipfile.ZipFile, info: zipfile.ZipInfo) -> int:
    """
    Calculate the data offset for a file in a ZIP archive.

    Args:
        zf (`zipfile.ZipFile`):
            The opened ZIP file. Must be opened in read mode.
        info (`zipfile.ZipInfo`):
            The file info.

    Returns:
        int: The offset of the file data in the ZIP archive.
    """
    if zf.fp is None:
        raise DDUFCorruptedFileError("ZipFile object must be opened in read mode.")

    # Step 1: Get the local file header offset
    header_offset = info.header_offset

    # Step 2: Read the local file header
    zf.fp.seek(header_offset)
    local_file_header = zf.fp.read(30)  # Fixed-size part of the local header

    if len(local_file_header) < 30:
        raise DDUFCorruptedFileError("Incomplete local file header.")

    # Step 3: Parse the header fields to calculate the start of file data
    # Local file header: https://en.wikipedia.org/wiki/ZIP_(file_format)#File_headers
    filename_len = int.from_bytes(local_file_header[26:28], "little")
    extra_field_len = int.from_bytes(local_file_header[28:30], "little")

    # Data offset is after the fixed header, filename, and extra fields
    data_offset = header_offset + 30 + filename_len + extra_field_len

    return data_offset

