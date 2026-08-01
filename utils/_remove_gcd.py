
def _remove_gcd(*x):
    try:
        g = igcd(*x)
    except ValueError:
        fx = list(filter(None, x))
        if len(fx) < 2:
            return x
        g = igcd(*[i.as_content_primitive()[0] for i in fx])
    except TypeError:
        raise TypeError('_remove_gcd(a,b,c) or _remove_gcd(*container)')
    if g == 1:
        return x
    return tuple([i//g for i in x])

