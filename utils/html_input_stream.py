
def HTMLInputStream(source, **kwargs):
    # Work around Python bug #20007: read(0) closes the connection.
    # http://bugs.python.org/issue20007
    if (isinstance(source, http_client.HTTPResponse) or
        # Also check for addinfourl wrapping HTTPResponse
        (isinstance(source, urllib.response.addbase) and
         isinstance(source.fp, http_client.HTTPResponse))):
        isUnicode = False
    elif hasattr(source, "read"):
        isUnicode = isinstance(source.read(0), text_type)
    else:
        isUnicode = isinstance(source, text_type)

    if isUnicode:
        encodings = [x for x in kwargs if x.endswith("_encoding")]
        if encodings:
            raise TypeError("Cannot set an encoding with a unicode input, set %r" % encodings)

        return HTMLUnicodeInputStream(source, **kwargs)
    else:
        return HTMLBinaryInputStream(source, **kwargs)

