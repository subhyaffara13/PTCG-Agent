
def parse_xread_resp3_to_resp2_legacy(response, **options):
    """RESP3-wire XREAD/XREADGROUP → legacy RESP2 ``list[[stream, entries]]``.

    Empty result ``{}`` is converted to ``[]`` to match today's RESP2 shape.
    """
    if not response:
        return []
    return [
        [key, parse_stream_list(value, **options)] for key, value in response.items()
    ]

