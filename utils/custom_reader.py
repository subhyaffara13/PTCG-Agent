
def custom_reader(file, format_name="all", filter_name="all", block_size=ffi.page_size):
    """Read an archive from a seekable file-like object.

    The `file` object must support the standard `readinto` and 'seek' methods.
    """
    buf = create_string_buffer(block_size)
    buf_p = cast(buf, c_void_p)

    def read_func(archive_p, context, ptrptr):
        # readinto the buffer, returns number of bytes read
        length = file.readinto(buf)
        # write the address of the buffer into the pointer
        ptrptr = cast(ptrptr, POINTER(c_void_p))
        ptrptr[0] = buf_p
        # tell libarchive how much data was written into the buffer
        return length

    def seek_func(archive_p, context, offset, whence):
        file.seek(offset, whence)
        # tell libarchvie the current position
        return file.tell()

    read_cb = ffi.READ_CALLBACK(read_func)
    seek_cb = SEEK_CALLBACK(seek_func)

    if new_api:
        open_cb = ffi.NO_OPEN_CB
        close_cb = ffi.NO_CLOSE_CB
    else:
        open_cb = libarchive.read.OPEN_CALLBACK(ffi.VOID_CB)
        close_cb = libarchive.read.CLOSE_CALLBACK(ffi.VOID_CB)

    with libarchive.read.new_archive_read(format_name, filter_name) as archive_p:
        read_set_seek_callback(archive_p, seek_cb)
        ffi.read_open(archive_p, None, open_cb, read_cb, close_cb)
        yield libarchive.read.ArchiveRead(archive_p)

