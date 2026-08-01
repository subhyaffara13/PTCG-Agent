
def parse_list_of_dicts_resp3(response, **kwargs):
    """Parse list-of-maps responses on RESP3 wire (e.g. ``XINFO`` family).

    Each list entry arrives as a ``dict`` with bytes keys; decode the
    keys to ``str`` so the Python shape matches what
    :func:`parse_list_of_dicts` produces from RESP2 wire.
    """
    return [{str_if_bytes(key): value for key, value in x.items()} for x in response]

