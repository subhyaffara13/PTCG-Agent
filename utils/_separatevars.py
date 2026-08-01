
def _separatevars(expr, force):
    if isinstance(expr, Abs):
        arg = expr.args[0]
        if arg.is_Mul and not arg.is_number:
            s = separatevars(arg, dict=True, force=force)
            if s is not None:
                return Mul(*map(expr.func, s.values()))
            else:
                return expr

    if len(expr.free_symbols) < 2:
        return expr

    # don't destroy a Mul since much of the work may already be done
    if expr.is_Mul:
        args = list(expr.args)
        changed = False
        for i, a in enumerate(args):
            args[i] = separatevars(a, force)
            changed = changed or args[i] != a
        if changed:
            expr = expr.func(*args)
        return expr

    # get a Pow ready for expansion
    if expr.is_Pow and expr.base != S.Exp1:
        expr = Pow(separatevars(expr.base, force=force), expr.exp)

    # First try other expansion methods
    expr = expr.expand(mul=False, multinomial=False, force=force)

    _expr, reps = posify(expr) if force else (expr, {})
    expr = factor(_expr).subs(reps)

    if not expr.is_Add:
        return expr

    # Find any common coefficients to pull out
    args = list(expr.args)
    commonc = args[0].args_cnc(cset=True, warn=False)[0]
    for i in args[1:]:
        commonc &= i.args_cnc(cset=True, warn=False)[0]
    commonc = Mul(*commonc)
    commonc = commonc.as_coeff_Mul()[1]  # ignore constants
    commonc_set = commonc.args_cnc(cset=True, warn=False)[0]

    # remove them
    for i, a in enumerate(args):
        c, nc = a.args_cnc(cset=True, warn=False)
        c = c - commonc_set
        args[i] = Mul(*c)*Mul(*nc)
    nonsepar = Add(*args)

    if len(nonsepar.free_symbols) > 1:
        _expr = nonsepar
        _expr, reps = posify(_expr) if force else (_expr, {})
        _expr = (factor(_expr)).subs(reps)

        if not _expr.is_Add:
            nonsepar = _expr

    return commonc*nonsepar

