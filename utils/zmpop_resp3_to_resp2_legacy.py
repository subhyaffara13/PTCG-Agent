
def zmpop_resp3_to_resp2_legacy(response, **options):
    """RESP3-wire ZMPOP/BZMPOP → legacy RESP2 ``[name, [[member, b"score"], ...]]``.

    Re-encodes RESP3 native float scores back to the bytes form Redis
    returns on the RESP2 wire so callers observe today's RESP2 raw shape.
    """
    if not response:
        return response
    return [
        response[0],
        [[member, _score_to_resp2_bytes(score)] for member, score in response[1]],
    ]

