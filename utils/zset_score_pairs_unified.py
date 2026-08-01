
def zset_score_pairs_unified(response, **options):
    """RESP2-wire WITHSCORES → unified ``list[[member, score], ...]``.

    Normalises RESP2 byte-string scores through ``float`` before applying
    ``score_cast_func`` so the cast receives the same input type as on a
    RESP3 connection.
    """
    if not response or not options.get("withscores"):
        return response
    score_cast_func = _wrap_score_cast_func(options.get("score_cast_func", float))
    it = iter(response)
    return [[val, score_cast_func(float(score))] for val, score in zip(it, it)]

