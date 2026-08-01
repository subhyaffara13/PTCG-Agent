
def trigsimp_old(expr, *, first=True, **opts):
    """
    Reduces expression by using known trig identities.

    Notes
    =====

    deep:
    - Apply trigsimp inside all objects with arguments

    recursive:
    - Use common subexpression elimination (cse()) and apply
    trigsimp recursively (this is quite expensive if the
    expression is large)

    method:
    - Determine the method to use. Valid choices are 'matching' (default),
    'groebner', 'combined', 'fu' and 'futrig'. If 'matching', simplify the
    expression recursively by pattern matching. If 'groebner', apply an
    experimental groebner basis algorithm. In this case further options
    are forwarded to ``trigsimp_groebner``, please refer to its docstring.
    If 'combined', first run the groebner basis algorithm with small
    default parameters, then run the 'matching' algorithm. 'fu' runs the
    collection of trigonometric transformations described by Fu, et al.
    (see the `fu` docstring) while `futrig` runs a subset of Fu-transforms
    that mimic the behavior of `trigsimp`.

    compare:
    - show input and output from `trigsimp` and `futrig` when different,
    but returns the `trigsimp` value.

    Examples
    ========

    >>> from sympy import trigsimp, sin, cos, log, cot
    >>> from sympy.abc import x
    >>> e = 2*sin(x)**2 + 2*cos(x)**2
    >>> trigsimp(e, old=True)
    2
    >>> trigsimp(log(e), old=True)
    log(2*sin(x)**2 + 2*cos(x)**2)
    >>> trigsimp(log(e), deep=True, old=True)
    log(2)

    Using `method="groebner"` (or `"combined"`) can sometimes lead to a lot
    more simplification:

    >>> e = (-sin(x) + 1)/cos(x) + cos(x)/(-sin(x) + 1)
    >>> trigsimp(e, old=True)
    (1 - sin(x))/cos(x) + cos(x)/(1 - sin(x))
    >>> trigsimp(e, method="groebner", old=True)
    2/cos(x)

    >>> trigsimp(1/cot(x)**2, compare=True, old=True)
          futrig: tan(x)**2
    cot(x)**(-2)

    """
    old = expr
    if first:
        if not expr.has(*_trigs):
            return expr

        trigsyms = set().union(*[t.free_symbols for t in expr.atoms(*_trigs)])
        if len(trigsyms) > 1:
            from sympy.simplify.simplify import separatevars

            d = separatevars(expr)
            if d.is_Mul:
                d = separatevars(d, dict=True) or d
            if isinstance(d, dict):
                expr = 1
                for v in d.values():
                    # remove hollow factoring
                    was = v
                    v = expand_mul(v)
                    opts['first'] = False
                    vnew = trigsimp(v, **opts)
                    if vnew == v:
                        vnew = was
                    expr *= vnew
                old = expr
            else:
                if d.is_Add:
                    for s in trigsyms:
                        r, e = expr.as_independent(s)
                        if r:
                            opts['first'] = False
                            expr = r + trigsimp(e, **opts)
                            if not expr.is_Add:
                                break
                    old = expr

    recursive = opts.pop('recursive', False)
    deep = opts.pop('deep', False)
    method = opts.pop('method', 'matching')

    def groebnersimp(ex, deep, **opts):
        def traverse(e):
            if e.is_Atom:
                return e
            args = [traverse(x) for x in e.args]
            if e.is_Function or e.is_Pow:
                args = [trigsimp_groebner(x, **opts) for x in args]
            return e.func(*args)
        if deep:
            ex = traverse(ex)
        return trigsimp_groebner(ex, **opts)

    trigsimpfunc = {
        'matching': (lambda x, d: _trigsimp(x, d)),
        'groebner': (lambda x, d: groebnersimp(x, d, **opts)),
        'combined': (lambda x, d: _trigsimp(groebnersimp(x,
                                       d, polynomial=True, hints=[2, tan]),
                                   d))
                   }[method]

    if recursive:
        w, g = cse(expr)
        g = trigsimpfunc(g[0], deep)

        for sub in reversed(w):
            g = g.subs(sub[0], sub[1])
            g = trigsimpfunc(g, deep)
        result = g
    else:
        result = trigsimpfunc(expr, deep)

    if opts.get('compare', False):
        f = futrig(old)
        if f != result:
            print('\tfutrig:', f)

    return result

