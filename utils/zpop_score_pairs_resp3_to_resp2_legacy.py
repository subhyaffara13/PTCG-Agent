
def zpop_score_pairs_resp3_to_resp2_legacy(response, **options):
    """RESP3-wire ZPOPMAX/ZPOPMIN → legacy RESP2 ``list[(member, score), ...]``.

    Both RESP3 shapes (flat without ``count``; nested with ``count``) are
    converted to a list of tuples. Scores are re-encoded to bytes before
    being passed to ``score_cast_func`` so the cast observes the same
    input type it would on a RESP2 connection.
    """
    if not response:
        return response
    score_cast_func = _wrap_score_cast_func(options.get("score_cast_func", float))
    if isinstance(response[0], list):
        return [
            (member, score_cast_func(_score_to_resp2_bytes(score)))
            for member, score in response
        ]
    return [(response[0], score_cast_func(_score_to_resp2_bytes(response[1])))]

