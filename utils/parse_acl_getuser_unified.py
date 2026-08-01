
def parse_acl_getuser_unified(response, **options):
    """ACL GETUSER → unified shape with selectors as ``list[dict]``.

    On RESP2 wire each selector arrives as a flat ``[k, v, k, v, …]``
    list; pair them into dicts to match the RESP3 wire shape.
    """
    data = parse_acl_getuser(response, **options)
    if data is None:
        return data
    selectors = data.get("selectors")
    if selectors and isinstance(selectors[0], list):
        data["selectors"] = [
            dict(zip(selector[0::2], selector[1::2])) for selector in selectors
        ]
    return data

