
def parse_client_trackinginfo_resp3_to_resp2_legacy(response, **options):
    """RESP3-wire CLIENT TRACKINGINFO → legacy RESP2 flat ``list``.

    Mirrors today's RESP2-wire callback (``list(map(str_if_bytes, r))``):
    labels are decoded to ``str`` while values are preserved as-is.
    """
    if not isinstance(response, dict):
        return list(map(str_if_bytes, response))
    out: list = []
    for key, value in response.items():
        out.append(str_if_bytes(key))
        out.append(value)
    return out

