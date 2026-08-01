
def hrandfield_resp3_to_resp2_legacy(response, **options):
    """RESP3-wire HRANDFIELD WITHVALUES → legacy RESP2 flat ``[field, value, ...]``.

    Plain (no-values) responses — flat list of fields — pass through.
    """
    if not response or not options.get("withvalues"):
        return response
    if not isinstance(response[0], list):
        return response
    flat = []
    for field, value in response:
        flat.append(field)
        flat.append(value)
    return flat

