
def _lin_eq2dict(a, symset):
    """return (c, d) where c is the sym-independent part of ``a`` and
    ``d`` is an efficiently calculated dictionary mapping symbols to
    their coefficients. A PolyNonlinearError is raised if non-linearity
    is detected.

    The values in the dictionary will be non-zero.

    Examples
    ========

    >>> from sympy.polys.matrices.linsolve import _lin_eq2dict
    >>> from sympy.abc import x, y
    >>> _lin_eq2dict(x + 2*y + 3, {x, y})
    (3, {x: 1, y: 2})
    """
    if a in symset:
        return S.Zero, {a: S.One}
    elif a.is_Add:
        terms_list = defaultdict(list)
        coeff_list = []
        for ai in a.args:
            ci, ti = _lin_eq2dict(ai, symset)
            coeff_list.append(ci)
            for mij, cij in ti.items():
                terms_list[mij].append(cij)
        coeff = Add(*coeff_list)
        terms = {sym: Add(*coeffs) for sym, coeffs in terms_list.items()}
        return coeff, terms
    elif a.is_Mul:
        terms = terms_coeff = None
        coeff_list = []
        for ai in a.args:
            ci, ti = _lin_eq2dict(ai, symset)
            if not ti:
                coeff_list.append(ci)
            elif terms is None:
                terms = ti
                terms_coeff = ci
            else:
                # since ti is not null and we already have
                # a term, this is a cross term
                raise PolyNonlinearError(filldedent('''
                    nonlinear cross-term: %s''' % a))
        coeff = Mul._from_args(coeff_list)
        if terms is None:
            return coeff, {}
        else:
            terms = {sym: coeff * c for sym, c in terms.items()}
            return  coeff * terms_coeff, terms
    elif not a.has_xfree(symset):
        return a, {}
    else:
        raise PolyNonlinearError('nonlinear term: %s' % a)

