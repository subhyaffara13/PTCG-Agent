
def _is_intent_callback(vdecl):
    for a in vdecl.get('attrspec', []):
        if _intentcallbackpattern.match(a):
            return 1
    return 0

