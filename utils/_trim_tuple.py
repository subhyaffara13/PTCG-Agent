
def _trim_tuple(a, b):
    a, b = _to_tuple(a, b)
    return tuple(a[0: 2] + a[len(a)//2 : len(a)//2 + 1] + a[-2:]), \
        tuple(b[0: 2] + b[len(b)//2 : len(b)//2 + 1] + b[-2:])

