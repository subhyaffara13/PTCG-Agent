
def get_indices(expr):
    """Determine the outer indices of expression ``expr``

    By *outer* we mean indices that are not summation indices.  Returns a set
    and a dict.  The set contains outer indices and the dict contains
    information about index symmetries.

    Examples
    ========

    >>> from sympy.tensor.index_methods import get_indices
    >>> from sympy import symbols
    >>> from sympy.tensor import IndexedBase
    >>> x, y, A = map(IndexedBase, ['x', 'y', 'A'])
    >>> i, j, a, z = symbols('i j a z', integer=True)

    The indices of the total expression is determined, Repeated indices imply a
    summation, for instance the trace of a matrix A:

    >>> get_indices(A[i, i])
    (set(), {})

    In the case of many terms, the terms are required to have identical
    outer indices.  Else an IndexConformanceException is raised.

    >>> get_indices(x[i] + A[i, j]*y[j])
    ({i}, {})

    :Exceptions:

    An IndexConformanceException means that the terms ar not compatible, e.g.

    >>> get_indices(x[i] + y[j])                #doctest: +SKIP
            (...)
    IndexConformanceException: Indices are not consistent: x(i) + y(j)

    .. warning::
       The concept of *outer* indices applies recursively, starting on the deepest
       level.  This implies that dummies inside parenthesis are assumed to be
       summed first, so that the following expression is handled gracefully:

       >>> get_indices((x[i] + A[i, j]*y[j])*x[j])
       ({i, j}, {})

       This is correct and may appear convenient, but you need to be careful
       with this as SymPy will happily .expand() the product, if requested.  The
       resulting expression would mix the outer ``j`` with the dummies inside
       the parenthesis, which makes it a different expression.  To be on the
       safe side, it is best to avoid such ambiguities by using unique indices
       for all contractions that should be held separate.

    """
    # We call ourself recursively to determine indices of sub expressions.

    # break recursion
    if isinstance(expr, Indexed):
        c = expr.indices
        inds, dummies = _remove_repeated(c)
        return inds, {}
    elif expr is None:
        return set(), {}
    elif isinstance(expr, Idx):
        return {expr}, {}
    elif expr.is_Atom:
        return set(), {}


    # recurse via specialized functions
    else:
        if expr.is_Mul:
            return _get_indices_Mul(expr)
        elif expr.is_Add:
            return _get_indices_Add(expr)
        elif expr.is_Pow or isinstance(expr, exp):
            return _get_indices_Pow(expr)

        elif isinstance(expr, Piecewise):
            # FIXME:  No support for Piecewise yet
            return set(), {}
        elif isinstance(expr, Function):
            # Support ufunc like behaviour by returning indices from arguments.
            # Functions do not interpret repeated indices across arguments
            # as summation
            ind0 = set()
            for arg in expr.args:
                ind, sym = get_indices(arg)
                ind0 |= ind
            return ind0, sym

        # this test is expensive, so it should be at the end
        elif not expr.has(Indexed):
            return set(), {}
        raise NotImplementedError(
            "FIXME: No specialized handling of type %s" % type(expr))


def get_indices(t):
    if not isinstance(t, TensExpr):
        return ()
    return t.get_indices()


def get_indices(targets, labels):
    return [get_index(t, labels) for t in targets]


def get_indices(grid, loop_index):
  indices = []
  for dim_size in reversed(grid):
    i = loop_index % dim_size
    loop_index = loop_index // dim_size
    indices.append(i)
  return tuple(reversed(indices))

