
def _has_varargs(func):
    if func not in signatures:
        return None
    sigs = signatures[func]
    checks = [check_varargs(sig) for sig in sigs]
    if all(checks):
        return True
    elif any(checks):
        return None
    return False

