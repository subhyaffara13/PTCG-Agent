
def parse_content_type(raw: str) -> tuple[str, MappingProxyType[str, str]]:
    """Parse Content-Type header.

    Returns a tuple of the parsed content type and a
    MappingProxyType of parameters. The default returned value
    is `application/octet-stream`
    """
    msg = HeaderParser(EnsureOctetStream, policy=HTTP).parsestr(f"Content-Type: {raw}")
    content_type = msg.get_content_type()
    params = msg.get_params(())
    content_dict = dict(params[1:])  # First element is content type again
    return content_type, MappingProxyType(content_dict)


def parse_content_type(header_value):
    """Parse a 'content-type' header value to get just the plain media-type (without parameters).

    This is done using the class Message from email.message as suggested in PEP 594
        (because the cgi is now deprecated and will be removed in python 3.13,
        see https://peps.python.org/pep-0594/#cgi).

    Args:
        header_value (str): The value of a 'content-type' header as a string.

    Returns:
        str: A string with just the lowercase media-type from the parsed 'content-type' header.
            If the provided content-type is not parsable, returns 'text/plain',
            the default value for textual files.
    """
    m = Message()
    m["content-type"] = header_value
    return (
        m.get_content_type()
    )  # Despite the name, actually returns just the media-type

