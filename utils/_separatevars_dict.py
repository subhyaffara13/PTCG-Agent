
def _separatevars_dict(expr, symbols):
    if symbols:
        if not all(t.is_Atom for t in symbols):
            raise ValueError("symbols must be Atoms.")
        symbols = list(symbols)
    elif symbols is None:
        return {'coeff': expr}
    else:
        symbols = list(expr.free_symbols)
        if not symbols:
            return None

    ret = {i: [] for i in symbols + ['coeff']}

    for i in Mul.make_args(expr):
        expsym = i.free_symbols
        intersection = set(symbols).intersection(expsym)
        if len(intersection) > 1:
            return None
        if len(intersection) == 0:
            # There are no symbols, so it is part of the coefficient
            ret['coeff'].append(i)
        else:
            ret[intersection.pop()].append(i)

    # rebuild
    for k, v in ret.items():
        ret[k] = Mul(*v)

    return ret

