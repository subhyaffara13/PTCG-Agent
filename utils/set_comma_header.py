from typing import List, Tuple

def set_comma_header(headers: Headers, name: bytes, new_values: List[bytes]) -> Headers:
    # The header name `name` is expected to be lower-case bytes.
    #
    # Note that when we store the header we use title casing for the header
    # names, in order to match the conventional HTTP header style.
    #
    # Simply calling `.title()` is a blunt approach, but it's correct
    # here given the cases where we're using `set_comma_header`...
    #
    # Connection, Content-Length, Transfer-Encoding.
    new_headers: List[Tuple[bytes, bytes]] = []
    for found_raw_name, found_name, found_raw_value in headers._full_items:
        if found_name != name:
            new_headers.append((found_raw_name, found_raw_value))
    for new_value in new_values:
        new_headers.append((name.title(), new_value))
    return normalize_and_validate(new_headers)

