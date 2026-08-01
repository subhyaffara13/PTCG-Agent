
def match_2nd_hypergeometric(eq, func):
    x = func.args[0]
    df = func.diff(x)
    a3 = Wild('a3', exclude=[func, func.diff(x), func.diff(x, 2)])
    b3 = Wild('b3', exclude=[func, func.diff(x), func.diff(x, 2)])
    c3 = Wild('c3', exclude=[func, func.diff(x), func.diff(x, 2)])
    deq = a3*(func.diff(x, 2)) + b3*df + c3*func
    r = collect(eq,
        [func.diff(x, 2), func.diff(x), func]).match(deq)
    if r:
        if not all(val.is_polynomial() for val in r.values()):
            n, d = eq.as_numer_denom()
            eq = expand(n)
            r = collect(eq, [func.diff(x, 2), func.diff(x), func]).match(deq)

    if r and r[a3]!=0:
        A = cancel(r[b3]/r[a3])
        B = cancel(r[c3]/r[a3])
        return [A, B]
    else:
        return []

