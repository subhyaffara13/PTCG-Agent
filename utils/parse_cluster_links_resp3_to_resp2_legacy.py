
def parse_cluster_links_resp3_to_resp2_legacy(response, **options):
    """RESP3-wire CLUSTER LINKS → today's RESP2 ``list[list]`` shape.

    Each link arrives as a ``dict`` with bytes keys; flatten back to
    interleaved ``[k, v, k, v, …]`` lists so the Python shape matches
    what RESP2 wire produces natively.
    """
    if response is None:
        return None
    return [
        [item for kv in link.items() for item in kv] if isinstance(link, dict) else link
        for link in response
    ]

