
def parse_range_unified(response, **kwargs):
    """Unified parser for TS.RANGE / TS.REVRANGE.

    Returns ``list[list]`` rather than ``list[tuple]`` so the unified
    shape is symmetric with the RESP3 wire format.
    """
    if not response:
        return []
    if len(response[0]) > 2:
        return [[r[0]] + [float(v) for v in r[1:]] for r in response]
    return [[r[0], float(r[1])] for r in response]

