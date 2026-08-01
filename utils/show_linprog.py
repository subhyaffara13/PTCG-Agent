
def show_linprog(c, A=None, b=None, A_eq=None, b_eq=None, bounds=None):
    from sympy import symbols
    ## the objective
    C = Matrix(c)
    if C.rows != 1 and C.cols == 1:
        C = C.T
    if C.rows != 1:
        raise ValueError("C must be a single row.")

    ## the inequalities
    if not A:
        if b:
            raise ValueError("A and b must both be given")
        # the governing equations will be simple constraints
        # on variables
        A, b = zeros(0, C.cols), zeros(C.cols, 1)
    else:
        A, b = [Matrix(i) for i in (A, b)]

    if A.cols != C.cols:
        raise ValueError("number of columns in A and C must match")

    ## the equalities
    if A_eq is None:
        if not b_eq is None:
            raise ValueError("A_eq and b_eq must both be given")
    else:
        A_eq, b_eq = [Matrix(i) for i in (A_eq, b_eq)]

    if not (bounds is None or bounds == {} or bounds == (0, None)):
        ## the bounds are interpreted
        if type(bounds) is tuple and len(bounds) == 2:
            bounds = [bounds] * A.cols
        elif len(bounds) == A.cols and all(
                type(i) is tuple and len(i) == 2 for i in bounds):
            pass # individual bounds
        elif type(bounds) is dict and all(
                type(i) is tuple and len(i) == 2
                for i in bounds.values()):
            # sparse bounds
            db = bounds
            bounds = [(0, None)] * A.cols
            while db:
                i, j = db.popitem()
                bounds[i] = j  # IndexError if out-of-bounds indices
        else:
            raise ValueError("unexpected bounds %s" % bounds)

    x = Matrix(symbols('x1:%s' % (A.cols+1)))
    f,c = (C*x)[0], [i<=j for i,j in zip(A*x, b)] + [Eq(i,j) for i,j in zip(A_eq*x,b_eq)]
    for i, (lo, hi) in enumerate(bounds):
        if lo is not None:
            c.append(x[i]>=lo)
        if hi is not None:
            c.append(x[i]<=hi)
    return f,c

