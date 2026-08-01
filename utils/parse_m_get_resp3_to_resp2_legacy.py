
def parse_m_get_resp3_to_resp2_legacy(response, **kwargs):
    """RESP3 wire → today's RESP2 legacy shape for TS.MGET."""
    res = []
    for key, item in response.items():
        labels = _nativestr_dict(item[0]) if item[0] else {}
        sample = item[1] if len(item) > 1 else []
        if not sample:
            res.append({nativestr(key): [labels, None, None]})
        else:
            res.append({nativestr(key): [labels, int(sample[0]), float(sample[1])]})
    return sorted(res, key=lambda d: list(d.keys()))

