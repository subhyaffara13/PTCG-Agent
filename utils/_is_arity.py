
def _is_arity(n, func):
    if func not in signatures:
        return None
    sigs = signatures[func]
    checks = [check_arity(n, sig) for sig in sigs]
    if all(checks):
        return True
    elif any(checks):
        return None
    return False

