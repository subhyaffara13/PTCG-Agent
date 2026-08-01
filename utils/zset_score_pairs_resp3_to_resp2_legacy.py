
def zset_score_pairs_resp3_to_resp2_legacy(response, **options):
    """Convert RESP3 nested ``[[member, score], ...]`` to today's RESP2
    ``list[(member, score)]`` shape: tuples instead of lists, scores
    re-encoded to bytes before being passed to ``score_cast_func`` so the
    cast receives the same input as on a RESP2 connection.
    """
    if not response or not options.get("withscores"):
        return response
    score_cast_func = _wrap_score_cast_func(options.get("score_cast_func", float))
    return [
        (member, score_cast_func(_score_to_resp2_bytes(score)))
        for member, score in response
    ]

