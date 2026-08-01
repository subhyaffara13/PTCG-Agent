
def parse_client_trackinginfo_unified(response, **options):
    """CLIENT TRACKINGINFO → unified ``dict[str, Any]``.

    Accepts either RESP2's flat ``[label, value, ...]`` list or RESP3's
    native ``dict`` and returns a ``dict`` with ``str`` keys.
    """
    if isinstance(response, dict):
        data = {str_if_bytes(key): value for key, value in response.items()}
    else:
        data = {
            str_if_bytes(key): value
            for key, value in zip(response[::2], response[1::2])
        }
    if "flags" in data:
        data["flags"] = [str_if_bytes(flag) for flag in data["flags"]]
    if "prefixes" in data:
        data["prefixes"] = [str_if_bytes(prefix) for prefix in data["prefixes"]]
    return data

