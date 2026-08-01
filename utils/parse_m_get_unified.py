
def parse_m_get_unified(response, **kwargs):
    """Unified parser for TS.MGET.

    Emits ``{key: [labels_dict, sample]}`` where ``sample`` is
    ``[int, float]`` or ``[]`` when no sample exists. Handles both wire
    formats: the RESP2 wire arrives as a list of ``[key, label_pairs,
    sample]`` triples; the RESP3 wire is already keyed by name.
    """
    if isinstance(response, dict):
        res = {}
        for key, item in response.items():
            sample = item[1] if len(item) > 1 else []
            if not sample:
                res[key] = [item[0], []]
            else:
                res[key] = [item[0], [int(sample[0]), float(sample[1])]]
        return res
    res = {}
    for item in response:
        if not item[2]:
            res[item[0]] = [_pairs_to_dict(item[1]), []]
        else:
            res[item[0]] = [
                _pairs_to_dict(item[1]),
                [int(item[2][0]), float(item[2][1])],
            ]
    return res

