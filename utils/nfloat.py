from typing import Dict

def nfloat(expr, n=15, exponent=False, dkeys=False):
    """Make all Rationals in expr Floats except those in exponents
    (unless the exponents flag is set to True) and those in undefined
    functions. When processing dictionaries, do not modify the keys
    unless ``dkeys=True``.

    Examples
    ========

    >>> from sympy import nfloat, cos, pi, sqrt
    >>> from sympy.abc import x, y
    >>> nfloat(x**4 + x/2 + cos(pi/3) + 1 + sqrt(y))
    x**4 + 0.5*x + sqrt(y) + 1.5
    >>> nfloat(x**4 + sqrt(y), exponent=True)
    x**4.0 + y**0.5

    Container types are not modified:

    >>> type(nfloat((1, 2))) is tuple
    True
    """
    from sympy.matrices.matrixbase import MatrixBase

    kw = {"n": n, "exponent": exponent, "dkeys": dkeys}

    if isinstance(expr, MatrixBase):
        return expr.applyfunc(lambda e: nfloat(e, **kw))

    # handling of iterable containers
    if iterable(expr, exclude=str):
        if isinstance(expr, (dict, Dict)):
            if dkeys:
                args = [tuple((nfloat(i, **kw) for i in a))
                    for a in expr.items()]
            else:
                args = [(k, nfloat(v, **kw)) for k, v in expr.items()]
            if isinstance(expr, dict):
                return type(expr)(args)
            else:
                return expr.func(*args)
        elif isinstance(expr, Basic):
            return expr.func(*[nfloat(a, **kw) for a in expr.args])
        return type(expr)([nfloat(a, **kw) for a in expr])

    rv = sympify(expr)

    if rv.is_Number:
        return Float(rv, n)
    elif rv.is_number:
        # evalf doesn't always set the precision
        rv = rv.n(n)
        if rv.is_Number:
            rv = Float(rv.n(n), n)
        else:
            pass  # pure_complex(rv) is likely True
        return rv
    elif rv.is_Atom:
        return rv
    elif rv.is_Relational:
        args_nfloat = (nfloat(arg, **kw) for arg in rv.args)
        return rv.func(*args_nfloat)


    # watch out for RootOf instances that don't like to have
    # their exponents replaced with Dummies and also sometimes have
    # problems with evaluating at low precision (issue 6393)
    from sympy.polys.rootoftools import RootOf
    rv = rv.xreplace({ro: ro.n(n) for ro in rv.atoms(RootOf)})

    from .power import Pow
    if not exponent:
        reps = [(p, Pow(p.base, Dummy())) for p in rv.atoms(Pow)]
        rv = rv.xreplace(dict(reps))
    rv = rv.n(n)
    if not exponent:
        rv = rv.xreplace({d.exp: p.exp for p, d in reps})
    else:
        # Pow._eval_evalf special cases Integer exponents so if
        # exponent is suppose to be handled we have to do so here
        rv = rv.xreplace(Transform(
            lambda x: Pow(x.base, Float(x.exp, n)),
            lambda x: x.is_Pow and x.exp.is_Integer))

    return rv.xreplace(Transform(
        lambda x: x.func(*nfloat(x.args, n, exponent)),
        lambda x: isinstance(x, Function) and not isinstance(x, AppliedUndef)))

