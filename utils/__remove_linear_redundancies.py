
def __remove_linear_redundancies(expr, Cs):
    cnts = {i: expr.count(i) for i in Cs}
    Cs = [i for i in Cs if cnts[i] > 0]

    def _linear(expr):
        if isinstance(expr, Add):
            xs = [i for i in Cs if expr.count(i)==cnts[i] \
                and 0 == expr.diff(i, 2)]
            d = {}
            for x in xs:
                y = expr.diff(x)
                if y not in d:
                    d[y]=[]
                d[y].append(x)
            for y in d:
                if len(d[y]) > 1:
                    d[y].sort(key=str)
                    for x in d[y][1:]:
                        expr = expr.subs(x, 0)
        return expr

    def _recursive_walk(expr):
        if len(expr.args) != 0:
            expr = expr.func(*[_recursive_walk(i) for i in expr.args])
        expr = _linear(expr)
        return expr

    if isinstance(expr, Equality):
        lhs, rhs = [_recursive_walk(i) for i in expr.args]
        f = lambda i: isinstance(i, Number) or i in Cs
        if isinstance(lhs, Symbol) and lhs in Cs:
            rhs, lhs = lhs, rhs
        if lhs.func in (Add, Symbol) and rhs.func in (Add, Symbol):
            dlhs = sift([lhs] if isinstance(lhs, AtomicExpr) else lhs.args, f)
            drhs = sift([rhs] if isinstance(rhs, AtomicExpr) else rhs.args, f)
            for i in [True, False]:
                for hs in [dlhs, drhs]:
                    if i not in hs:
                        hs[i] = [0]
            # this calculation can be simplified
            lhs = Add(*dlhs[False]) - Add(*drhs[False])
            rhs = Add(*drhs[True]) - Add(*dlhs[True])
        elif lhs.func in (Mul, Symbol) and rhs.func in (Mul, Symbol):
            dlhs = sift([lhs] if isinstance(lhs, AtomicExpr) else lhs.args, f)
            if True in dlhs:
                if False not in dlhs:
                    dlhs[False] = [1]
                lhs = Mul(*dlhs[False])
                rhs = rhs/Mul(*dlhs[True])
        return Eq(lhs, rhs)
    else:
        return _recursive_walk(expr)

