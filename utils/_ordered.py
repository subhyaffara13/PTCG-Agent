
def _ordered(u, v):
    """Returns the nodes in an undirected edge in lower-triangular order"""
    return (u, v) if u < v else (v, u)

