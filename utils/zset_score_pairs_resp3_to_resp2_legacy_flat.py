
def zset_score_pairs_resp3_to_resp2_legacy_flat(response, **options):
    """Convert RESP3 nested ``[[member, score], ...]`` to the flat raw RESP2
    wire shape ``[member, score_bytes, ...]`` used by ZDIFF in v8.0.0b1.

    ZDIFF historically did not propagate ``withscores`` to the response
    callback, so the legacy RESP2 callback was a no-op and the raw flat
    wire response was returned to the user. This helper reproduces that
    shape on RESP3 wires so ``legacy_responses=True`` keeps emitting the
    same Python value regardless of the underlying protocol.
    """
    if not response or not options.get("withscores"):
        return response
    flat = []
    for member, score in response:
        flat.append(member)
        flat.append(_score_to_resp2_bytes(score))
    return flat

