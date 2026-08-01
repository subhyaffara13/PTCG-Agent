
def parse_acl_getuser_resp3_to_resp2_legacy(response, **options):
    """RESP3-wire ACL GETUSER → today's RESP2 selectors as flat lists.

    Each selector arrives as a ``dict`` on RESP3 wire; flatten back to
    the interleaved ``[k, v, k, v, …]`` form produced by RESP2 wire.
    """
    data = parse_acl_getuser(response, **options)
    if data is None:
        return data
    selectors = data.get("selectors")
    if selectors and isinstance(selectors[0], dict):
        data["selectors"] = [
            [item for kv in selector.items() for item in kv] for selector in selectors
        ]
    return data

