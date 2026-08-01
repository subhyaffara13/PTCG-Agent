
def coerce(x,y):
    if x not in 'fdFD':
        x = 'd'
    if y not in 'fdFD':
        y = 'd'
    return _coerce_rules[x,y]


def coerce(request):
    return request.param


def coerce(request):
    """Coerce input to strings or raise an error for non-string input"""
    return request.param

