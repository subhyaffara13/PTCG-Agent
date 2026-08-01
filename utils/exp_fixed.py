
def exp_fixed(x, prec, ln2=None):
    if ln2 is None:
        ln2 = ln2_fixed(prec)
    n, t = divmod(x, ln2)
    n = int(n)
    v = exp_basecase(t, prec)
    if n >= 0:
        return v << n
    else:
        return v >> (-n)

