
def _linsolve(eqs, syms):

    """Solve a linear system of equations.

    Examples
    ========

    Solve a linear system with a unique solution:

    >>> from sympy import symbols, Eq
    >>> from sympy.polys.matrices.linsolve import _linsolve
    >>> x, y = symbols('x, y')
    >>> eqs = [Eq(x + y, 1), Eq(x - y, 2)]
    >>> _linsolve(eqs, [x, y])
    {x: 3/2, y: -1/2}

    In the case of underdetermined systems the solution will be expressed in
    terms of the unknown symbols that are unconstrained:

    >>> _linsolve([Eq(x + y, 0)], [x, y])
    {x: -y, y: y}

    """
    # Number of unknowns (columns in the non-augmented matrix)
    nsyms = len(syms)

    # Convert to sparse augmented matrix (len(eqs) x (nsyms+1))
    eqsdict, const = _linear_eq_to_dict(eqs, syms)
    Aaug = sympy_dict_to_dm(eqsdict, const, syms)
    K = Aaug.domain

    # sdm_irref has issues with float matrices. This uses the ddm_rref()
    # function. When sdm_rref() can handle float matrices reasonably this
    # should be removed...
    if K.is_RealField or K.is_ComplexField:
        Aaug = Aaug.to_ddm().rref()[0].to_sdm()

    # Compute reduced-row echelon form (RREF)
    Arref, pivots, nzcols = sdm_irref(Aaug)

    # No solution:
    if pivots and pivots[-1] == nsyms:
        return None

    # Particular solution for non-homogeneous system:
    P = sdm_particular_from_rref(Arref, nsyms+1, pivots)

    # Nullspace - general solution to homogeneous system
    # Note: using nsyms not nsyms+1 to ignore last column
    V, nonpivots = sdm_nullspace_from_rref(Arref, K.one, nsyms, pivots, nzcols)

    # Collect together terms from particular and nullspace:
    sol = defaultdict(list)
    for i, v in P.items():
        sol[syms[i]].append(K.to_sympy(v))
    for npi, Vi in zip(nonpivots, V):
        sym = syms[npi]
        for i, v in Vi.items():
            sol[syms[i]].append(sym * K.to_sympy(v))

    # Use a single call to Add for each term:
    sol = {s: Add(*terms) for s, terms in sol.items()}

    # Fill in the zeros:
    zero = S.Zero
    for s in set(syms) - set(sol):
        sol[s] = zero

    # All done!
    return sol


def _linsolve(p):
    # Compute root of linear polynomial.
    c, d = p.rep.to_list()
    return -d/c

