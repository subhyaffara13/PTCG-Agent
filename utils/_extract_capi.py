
def _extract_capi(module):
    """Return {name: signature} for every entry in module.__pyx_capi__."""
    result = {}
    for name, capsule in module.__pyx_capi__.items():
        raw = _get_capsule_name(capsule)
        if raw is not None:
            result[name] = raw.decode('utf-8')
    return result


def _extract_capi(module):
    """Return {name: signature} for every entry in module.__pyx_capi__."""
    result = {}
    for name, capsule in module.__pyx_capi__.items():
        raw = _get_capsule_name(capsule)
        if raw is not None:
            result[name] = raw.decode('utf-8')
    return result


def _extract_capi(module):
    """Return {name: signature} for every entry in module.__pyx_capi__."""
    result = {}
    for name, capsule in module.__pyx_capi__.items():
        raw = _get_capsule_name(capsule)
        if raw is not None:
            result[name] = raw.decode('utf-8')
    return result

