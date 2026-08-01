
def _num_required_args(func):
    if func not in signatures:
        return None
    sigs = signatures[func]
    vals = [check_required_args(sig) for sig in sigs]
    val = vals[0]
    if all(x == val for x in vals):
        return val
    return None

