
def parse_m_range(response, **kwargs):
    """Parse multi range response (RESP2 wire)."""
    res = []
    for item in response:
        res.append({nativestr(item[0]): [list_to_dict(item[1]), parse_range(item[2])]})
    return sorted(res, key=lambda d: list(d.keys()))

