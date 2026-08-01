
def zset_score_for_rank_unified(response, **options):
    """RESP2-wire ZRANK/ZREVRANK WITHSCORE → unified ``[rank, score]``.

    Normalises the RESP2 byte-string score through ``float`` before
    applying ``score_cast_func`` so the cast receives the same input type
    as on a RESP3 connection.
    """
    if not response or not options.get("withscore"):
        return response
    score_cast_func = _wrap_score_cast_func(options.get("score_cast_func", float))
    return [response[0], score_cast_func(float(response[1]))]

