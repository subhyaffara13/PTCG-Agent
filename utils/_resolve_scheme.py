
def _resolve_scheme(name):
    os_name, sep, key = name.partition('_')
    try:
        resolved = sysconfig.get_preferred_scheme(key)
    except Exception:
        resolved = fw.scheme(name)
    return resolved

