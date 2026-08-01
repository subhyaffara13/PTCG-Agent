
def parse_lcs_idx_resp3_to_resp2_legacy(response, **options):
    """RESP3-wire LCS with IDX → legacy RESP2 flat list shape.

    Reproduces today's RESP2 raw output (``[b"matches", [...], b"len", n]``).
    Non-IDX responses pass through unchanged.
    """
    if not isinstance(response, dict):
        return response
    out: list = []
    for key, value in response.items():
        out.append(key)
        out.append(value)
    return out

