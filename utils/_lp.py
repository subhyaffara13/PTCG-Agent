
def _lp(min_max, f, constr):
    """Return the optimization (min or max) of ``f`` with the given
    constraints. All variables are unbounded unless constrained.

    If `min_max` is 'max' then the results corresponding to the
    maximization of ``f`` will be returned, else the minimization.
    The constraints can be given as Le, Ge or Eq expressions.

    Examples
    ========

    >>> from sympy.solvers.simplex import _lp as lp
    >>> from sympy import Eq
    >>> from sympy.abc import x, y, z
    >>> f = x + y - 2*z
    >>> c = [7*x + 4*y - 7*z <= 3, 3*x - y + 10*z <= 6]
    >>> c += [i >= 0 for i in (x, y, z)]
    >>> lp(min, f, c)
    (-6/5, {x: 0, y: 0, z: 3/5})

    By passing max, the maximum value for f under the constraints
    is returned (if possible):

    >>> lp(max, f, c)
    (3/4, {x: 0, y: 3/4, z: 0})

    Constraints that are equalities will require that the solution
    also satisfy them:

    >>> lp(max, f, c + [Eq(y - 9*x, 1)])
    (5/7, {x: 0, y: 1, z: 1/7})

    All symbols are reported, even if they are not in the objective
    function:

    >>> lp(min, x, [y + x >= 3, x >= 0])
    (0, {x: 0, y: 3})
    """
    # get the matrix components for the system expressed
    # in terms of only nonnegative variables
    A, B, C, D, r, xx, aux = _lp_matrices(f, constr)

    how = str(min_max).lower()
    if "max" in how:
        # _simplex minimizes for Ax <= B so we
        # have to change the sign of the function
        # and negate the optimal value returned
        _o, p, d = _simplex(A, B, -C, -D)
        o = -_o
    elif "min" in how:
        o, p, d = _simplex(A, B, C, D)
    else:
        raise ValueError("expecting min or max")

    # restore original variables and remove aux from p
    p = dict(zip(xx, p))
    if r:  # p has original symbols and auxilliary symbols
        # if r has x: x - z1 use values from p to update
        r = {k: v.xreplace(p) for k, v in r.items()}
        # then use the actual value of x (= x - z1) in p
        p.update(r)
        # don't show aux
        p = {k: p[k] for k in ordered(p) if k not in aux}

    # not returning dual since there may be extra constraints
    # when a variable has finite bounds
    return o, p

