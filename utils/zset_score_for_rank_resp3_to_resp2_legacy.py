
def zset_score_for_rank_resp3_to_resp2_legacy(response, **options):
    """RESP3-wire ZRANK/ZREVRANK WITHSCORE → legacy RESP2 ``[rank, score]``.

    The shape ``[rank, score]`` is identical between RESP2 and RESP3; only
    the score is re-encoded to bytes before being passed to
    ``score_cast_func`` so the cast observes the same input type it would
    on a RESP2 connection.
    """
    if not response or not options.get("withscore"):
        return response
    score_cast_func = _wrap_score_cast_func(options.get("score_cast_func", float))
    return [response[0], score_cast_func(_score_to_resp2_bytes(response[1]))]

