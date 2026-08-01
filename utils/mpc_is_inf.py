
def mpc_is_inf(z):
    """Check if either real or imaginary part is infinite"""
    re, im = z
    if re in _infs: return True
    if im in _infs: return True
    return False

