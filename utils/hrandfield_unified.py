
def hrandfield_unified(response, **options):
    """RESP2-wire HRANDFIELD WITHVALUES → unified ``list[[field, value], ...]``.

    Plain (no-values) responses — flat list of fields — pass through.
    The ``withvalues`` option (forwarded by the command method) selects the
    pairing branch so the no-values flat result is never misread.
    """
    if not response or not options.get("withvalues"):
        return response
    if isinstance(response[0], list):
        return response
    it = iter(response)
    return [[field, value] for field, value in zip(it, it)]

