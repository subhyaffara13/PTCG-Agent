
def as_numer_denom(obj):
    """Return expression as numer-denom pair.
    """
    if isinstance(obj, Expr):
        obj = normalize(obj)
        if obj.op in (Op.INTEGER, Op.REAL, Op.COMPLEX, Op.SYMBOL,
                      Op.INDEXING, Op.TERNARY):
            return obj, as_number(1)
        elif obj.op is Op.APPLY:
            if obj.data[0] is ArithOp.DIV and not obj.data[2]:
                numers, denoms = map(as_numer_denom, obj.data[1])
                return numers[0] * denoms[1], numers[1] * denoms[0]
            return obj, as_number(1)
        elif obj.op is Op.TERMS:
            numers, denoms = [], []
            for term, coeff in obj.data.items():
                n, d = as_numer_denom(term)
                n = n * coeff
                numers.append(n)
                denoms.append(d)
            numer, denom = as_number(0), as_number(1)
            for i in range(len(numers)):
                n = numers[i]
                for j in range(len(numers)):
                    if i != j:
                        n *= denoms[j]
                numer += n
                denom *= denoms[i]
            if denom.op in (Op.INTEGER, Op.REAL) and denom.data[0] < 0:
                numer, denom = -numer, -denom
            return numer, denom
        elif obj.op is Op.FACTORS:
            numer, denom = as_number(1), as_number(1)
            for b, e in obj.data.items():
                bnumer, bdenom = as_numer_denom(b)
                if e > 0:
                    numer *= bnumer ** e
                    denom *= bdenom ** e
                elif e < 0:
                    numer *= bdenom ** (-e)
                    denom *= bnumer ** (-e)
            return numer, denom
    raise OpError(f'cannot convert {type(obj)} to numer and denom')

