
def _normal_ordered_form_factor(product, independent=False, recursive_limit=10,
                                _recursive_depth=0):
    """
    Helper function for normal_ordered_form_factor: Write multiplication
    expression with bosonic or fermionic operators on normally ordered form,
    using the bosonic and fermionic commutation relations. The resulting
    operator expression is equivalent to the argument, but will in general be
    a sum of operator products instead of a simple product.
    """

    factors = _expand_powers(product)

    new_factors = []
    n = 0
    while n < len(factors) - 1:
        current, next = factors[n], factors[n + 1]
        if any(not isinstance(f, (FermionOp, BosonOp)) for f in (current, next)):
            new_factors.append(current)
            n += 1
            continue

        key_1 = (current.is_annihilation, str(current.name))
        key_2 = (next.is_annihilation, str(next.name))

        if key_1 <= key_2:
            new_factors.append(current)
            n += 1
            continue

        n += 2
        if current.is_annihilation and not next.is_annihilation:
            if isinstance(current, BosonOp) and isinstance(next, BosonOp):
                if current.args[0] != next.args[0]:
                    if independent:
                        c = 0
                    else:
                        c = Commutator(current, next)
                    new_factors.append(next * current + c)
                else:
                    new_factors.append(next * current + 1)
            elif isinstance(current, FermionOp) and isinstance(next, FermionOp):
                if current.args[0] != next.args[0]:
                    if independent:
                        c = 0
                    else:
                        c = AntiCommutator(current, next)
                    new_factors.append(-next * current + c)
                else:
                    new_factors.append(-next * current + 1)
        elif (current.is_annihilation == next.is_annihilation and
            isinstance(current, FermionOp) and isinstance(next, FermionOp)):
            new_factors.append(-next * current)
        else:
            new_factors.append(next * current)

    if n == len(factors) - 1:
        new_factors.append(factors[-1])

    if new_factors == factors:
        return product
    else:
        expr = Mul(*new_factors).expand()
        return normal_ordered_form(expr,
                                   recursive_limit=recursive_limit,
                                   _recursive_depth=_recursive_depth + 1,
                                   independent=independent)

