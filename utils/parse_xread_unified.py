
def parse_xread_unified(response, **options):
    """XREAD/XREADGROUP → unified ``dict[stream, list[tuple[id, dict]]]``.

    Accepts either RESP2 (``list[[stream, entries]]``) or RESP3
    (``dict[stream, entries]``) wire shape. Empty result is ``{}``.
    """
    if not response:
        return {}
    if isinstance(response, dict):
        return {
            key: parse_stream_list(value, **options) for key, value in response.items()
        }
    return {
        stream: parse_stream_list(entries, **options) for stream, entries in response
    }

