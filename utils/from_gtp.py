
def from_gtp(gtpc):
    """Converts from a GTP coordinate to a Minigo coordinate."""
    gtpc = gtpc.upper()
    if gtpc == "PASS":
        return None
    col = _GTP_COLUMNS.index(gtpc[0])
    row_from_bottom = int(gtpc[1:])
    return go_base.N - row_from_bottom, col

