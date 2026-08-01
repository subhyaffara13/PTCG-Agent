
def parse_m_get(response):
    """Parse multi get response (RESP2 wire)."""
    res = []
    for item in response:
        if not item[2]:
            res.append({nativestr(item[0]): [list_to_dict(item[1]), None, None]})
        else:
            res.append(
                {
                    nativestr(item[0]): [
                        list_to_dict(item[1]),
                        int(item[2][0]),
                        float(item[2][1]),
                    ]
                }
            )
    return sorted(res, key=lambda d: list(d.keys()))

