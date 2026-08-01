
def _replace_mul_fpowxgpow(expr, f, g, rexp, h, rexph):
    """Helper for _match_div_rewrite.

    Replace f(b_)**c_*g(b_)**(rexp(c_)) with h(b)**rexph(c) if f(b_)
    and g(b_) are both positive or if c_ is an integer.
    """
    # assert expr.is_Mul and expr.is_commutative and f != g
    fargs = defaultdict(int)
    gargs = defaultdict(int)
    args = []
    for x in expr.args:
        if x.is_Pow or x.func in (f, g):
            b, e = x.as_base_exp()
            if b.is_positive or e.is_integer:
                if b.func == f:
                    fargs[b.args[0]] += e
                    continue
                elif b.func == g:
                    gargs[b.args[0]] += e
                    continue
        args.append(x)
    common = set(fargs) & set(gargs)
    hit = False
    while common:
        key = common.pop()
        fe = fargs.pop(key)
        ge = gargs.pop(key)
        if fe == rexp(ge):
            args.append(h(key)**rexph(fe))
            hit = True
        else:
            fargs[key] = fe
            gargs[key] = ge
    if not hit:
        return expr
    while fargs:
        key, e = fargs.popitem()
        args.append(f(key)**e)
    while gargs:
        key, e = gargs.popitem()
        args.append(g(key)**e)
    return Mul(*args)

