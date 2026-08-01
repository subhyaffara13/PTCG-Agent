
def parse_m_range_unified(response, **kwargs):
    """Unified parser for TS.MRANGE / TS.MREVRANGE.

    Emits ``{key: [labels_dict, metadata, samples]}`` regardless of wire
    format. RESP2 has no metadata element on the wire, so the command options
    are used to synthesize the same ``{"aggregators": ...}`` structure that
    RESP3 returns.
    """
    if isinstance(response, dict):
        res = {}
        for key, item in response.items():
            metadata = item[1] if len(item) > 2 else []
            res[key] = [item[0], metadata, parse_range_unified(item[-1])]
        return res
    res = {}
    metadata = _m_range_metadata(kwargs.get("aggregation_type"))
    for item in response:
        res[item[0]] = [
            _pairs_to_dict(item[1]),
            metadata,
            parse_range_unified(item[2]),
        ]
    return res

