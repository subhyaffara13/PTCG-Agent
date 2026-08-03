import os

def _copy_file_contents(src, dst, buffer_size=16 * 1024):  # noqa: C901
    """Copy the file 'src' to 'dst'; both must be filenames.  Any error
    opening either file, reading from 'src', or writing to 'dst', raises
    DistutilsFileError.  Data is read/written in chunks of 'buffer_size'
    bytes (default 16k).  No attempt is made to handle anything apart from
    regular files.
    """
    # Stolen from shutil module in the standard library, but with
    # custom error-handling added.
    fsrc = None
    fdst = None
    try:
        try:
            fsrc = open(src, 'rb')
        except OSError as e:
            raise DistutilsFileError(f"could not open '{src}': {e.strerror}")

        if os.path.exists(dst):
            try:
                os.unlink(dst)
            except OSError as e:
                raise DistutilsFileError(f"could not delete '{dst}': {e.strerror}")

        try:
            fdst = open(dst, 'wb')
        except OSError as e:
            raise DistutilsFileError(f"could not create '{dst}': {e.strerror}")

        while True:
            try:
                buf = fsrc.read(buffer_size)
            except OSError as e:
                raise DistutilsFileError(f"could not read from '{src}': {e.strerror}")

            if not buf:
                break

            try:
                fdst.write(buf)
            except OSError as e:
                raise DistutilsFileError(f"could not write to '{dst}': {e.strerror}")
    finally:
        if fdst:
            fdst.close()
        if fsrc:
            fsrc.close()

