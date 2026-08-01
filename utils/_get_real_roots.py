
def _get_real_roots(f, x):
    """get real roots of f if possible"""
    rs = roots(f, filter='R')

    try:
        num_roots = f.count_roots()
    except DomainError:
        return rs
    else:
        if len(rs) == num_roots:
            return rs
        else:
            return None

