
def split_commutative_parts(e):
    """Split into commutative and non-commutative parts."""
    c_part, nc_part = e.args_cnc()
    c_part = list(c_part)
    return c_part, nc_part

