
def parse_lcs_idx_unified(response, **options):
    """LCS with IDX → unified ``dict``.

    Used for the ``legacy_responses=False`` overlay on RESP2 wire to mirror
    RESP3's native ``dict`` shape. Non-IDX responses (``bytes`` / ``int``)
    pass through unchanged.
    """
    if isinstance(response, list):
        it = iter(response)
        return {str_if_bytes(key): value for key, value in zip(it, it)}
    if isinstance(response, dict):
        return {str_if_bytes(key): value for key, value in response.items()}
    return response

