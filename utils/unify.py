
def unify(u, v, s):  # no check at the moment
    """Find substitution so that u == v while satisfying s
    >>> x = var("x")
    >>> unify((1, x), (1, 2), {})
    {~x: 2}
    """
    u = walk(u, s)
    v = walk(v, s)
    if u == v:
        return s
    if isvar(u):
        return assoc(s, u, v)
    if isvar(v):
        return assoc(s, v, u)
    return _unify(u, v, s)


def unify(u, v):
    return unify(u, v, {})


def unify(x, y, s=None, **fns):
    """ Unify two expressions.

    Parameters
    ==========

        x, y - expression trees containing leaves, Compounds and Variables.
        s    - a mapping of variables to subtrees.

    Returns
    =======

        lazy sequence of mappings {Variable: subtree}

    Examples
    ========

    >>> from sympy.unify.core import unify, Compound, Variable
    >>> expr    = Compound("Add", ("x", "y"))
    >>> pattern = Compound("Add", ("x", Variable("a")))
    >>> next(unify(expr, pattern, {}))
    {Variable(a): 'y'}
    """
    s = s or {}

    if x == y:
        yield s
    elif isinstance(x, (Variable, CondVariable)):
        yield from unify_var(x, y, s, **fns)
    elif isinstance(y, (Variable, CondVariable)):
        yield from unify_var(y, x, s, **fns)
    elif isinstance(x, Compound) and isinstance(y, Compound):
        is_commutative = fns.get('is_commutative', lambda x: False)
        is_associative = fns.get('is_associative', lambda x: False)
        for sop in unify(x.op, y.op, s, **fns):
            if is_associative(x) and is_associative(y):
                a, b = (x, y) if len(x.args) < len(y.args) else (y, x)
                if is_commutative(x) and is_commutative(y):
                    combs = allcombinations(a.args, b.args, 'commutative')
                else:
                    combs = allcombinations(a.args, b.args, 'associative')
                for aaargs, bbargs in combs:
                    aa = [unpack(Compound(a.op, arg)) for arg in aaargs]
                    bb = [unpack(Compound(b.op, arg)) for arg in bbargs]
                    yield from unify(aa, bb, sop, **fns)
            elif len(x.args) == len(y.args):
                yield from unify(x.args, y.args, sop, **fns)

    elif is_args(x) and is_args(y) and len(x) == len(y):
        if len(x) == 0:
            yield s
        else:
            for shead in unify(x[0], y[0], s, **fns):
                yield from unify(x[1:], y[1:], shead, **fns)


def unify(x, y, s=None, variables=(), **kwargs):
    """ Structural unification of two expressions/patterns.

    Examples
    ========

    >>> from sympy.unify.usympy import unify
    >>> from sympy import Basic, S
    >>> from sympy.abc import x, y, z, p, q

    >>> next(unify(Basic(S(1), S(2)), Basic(S(1), x), variables=[x]))
    {x: 2}

    >>> expr = 2*x + y + z
    >>> pattern = 2*p + q
    >>> next(unify(expr, pattern, {}, variables=(p, q)))
    {p: x, q: y + z}

    Unification supports commutative and associative matching

    >>> expr = x + y + z
    >>> pattern = p + q
    >>> len(list(unify(expr, pattern, {}, variables=(p, q))))
    12

    Symbols not indicated to be variables are treated as literal,
    else they are wild-like and match anything in a sub-expression.

    >>> expr = x*y*z + 3
    >>> pattern = x*y + 3
    >>> next(unify(expr, pattern, {}, variables=[x, y]))
    {x: y, y: x*z}

    The x and y of the pattern above were in a Mul and matched factors
    in the Mul of expr. Here, a single symbol matches an entire term:

    >>> expr = x*y + 3
    >>> pattern = p + 3
    >>> next(unify(expr, pattern, {}, variables=[p]))
    {p: x*y}

    """
    decons = lambda x: deconstruct(x, variables)
    s = s or {}
    s = {decons(k): decons(v) for k, v in s.items()}

    ds = core.unify(decons(x), decons(y), s,
                                     is_associative=is_associative,
                                     is_commutative=is_commutative,
                                     **kwargs)
    for d in ds:
        yield {construct(k): construct(v) for k, v in d.items()}


def unify(a, b, s={}):
    return core.unify(a, b, s=s, is_associative=is_associative,
                          is_commutative=is_commutative)


def unify(K0, K1):
    return K0.unify(K1)

