
def canon_bp(p):
    """
    Butler-Portugal canonicalization. See ``tensor_can.py`` from the
    combinatorics module for the details.
    """
    if isinstance(p, TensExpr):
        return p.canon_bp()
    return p

