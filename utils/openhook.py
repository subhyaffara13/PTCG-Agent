
def openhook(filename, mode):
    """Ensures that filename is opened with correct encoding parameter.

    This function uses charset_normalizer package, when available, for
    determining the encoding of the file to be opened. When charset_normalizer
    is not available, the function detects only UTF encodings, otherwise, ASCII
    encoding is used as fallback.
    """
    # Reads in the entire file. Robust detection of encoding.
    # Correctly handles comments or late stage unicode characters
    # gh-22871
    if charset_normalizer is not None:
        encoding = charset_normalizer.from_path(filename).best().encoding
    else:
        # hint: install charset_normalizer for correct encoding handling
        # No need to read the whole file for trying with startswith
        nbytes = min(32, os.path.getsize(filename))
        with open(filename, 'rb') as fhandle:
            raw = fhandle.read(nbytes)
            if raw.startswith(codecs.BOM_UTF8):
                encoding = 'UTF-8-SIG'
            elif raw.startswith((codecs.BOM_UTF32_LE, codecs.BOM_UTF32_BE)):
                encoding = 'UTF-32'
            elif raw.startswith((codecs.BOM_LE, codecs.BOM_BE)):
                encoding = 'UTF-16'
            else:
                # Fallback, without charset_normalizer
                encoding = 'ascii'
    return open(filename, mode, encoding=encoding)

