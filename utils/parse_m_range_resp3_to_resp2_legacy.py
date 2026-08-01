
def parse_m_range_resp3_to_resp2_legacy(response, **kwargs):
    """RESP3 wire → today's RESP2 legacy shape for TS.MRANGE / TS.MREVRANGE."""
    res = []
    for key, item in response.items():
        labels = _nativestr_dict(item[0]) if item[0] else {}
        samples = item[-1]
        res.append({nativestr(key): [labels, parse_range(samples)]})
    return sorted(res, key=lambda d: list(d.keys()))

