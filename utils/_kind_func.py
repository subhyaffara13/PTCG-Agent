
def _kind_func(string):
    # XXX: return something sensible.
    if string[0] in "'\"":
        string = string[1:-1]
    if real16pattern.match(string):
        return 8
    elif real8pattern.match(string):
        return 4
    return 'kind(' + string + ')'

