
def parse_cluster_links_unified(response, **options):
    """CLUSTER LINKS → unified ``list[dict]`` with string keys.

    Accepts either RESP2 wire (``list[list]`` of flat pairs) or RESP3
    wire (``list[dict]``). Both are normalised to ``list[dict]``.
    """
    if response is None:
        return None
    return [
        {str_if_bytes(k): v for k, v in item.items()}
        if isinstance(item, dict)
        else pairs_to_dict(item, decode_keys=True)
        for item in response
    ]

