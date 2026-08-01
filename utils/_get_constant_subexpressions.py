
def _get_constant_subexpressions(expr, Cs):
    Cs = set(Cs)
    Ces = []
    def _recursive_walk(expr):
        expr_syms = expr.free_symbols
        if expr_syms and expr_syms.issubset(Cs):
            Ces.append(expr)
        else:
            if expr.func == exp:
                expr = expr.expand(mul=True)
            if expr.func in (Add, Mul):
                d = sift(expr.args, lambda i : i.free_symbols.issubset(Cs))
                if len(d[True]) > 1:
                    x = expr.func(*d[True])
                    if not x.is_number:
                        Ces.append(x)
            elif isinstance(expr, Integral):
                if expr.free_symbols.issubset(Cs) and \
                            all(len(x) == 3 for x in expr.limits):
                    Ces.append(expr)
            for i in expr.args:
                _recursive_walk(i)
        return
    _recursive_walk(expr)
    return Ces

