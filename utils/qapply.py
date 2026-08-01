
def qapply(e, **options):
    """Apply operators to states in a quantum expression.

    Parameters
    ==========

    e : Expr
        The expression containing operators and states. This expression tree
        will be walked to find operators acting on states symbolically.
    options : dict
        A dict of key/value pairs that determine how the operator actions
        are carried out.

        The following options are valid:

        * ``dagger``: try to apply Dagger operators to the left
          (default: False).
        * ``ip_doit``: call ``.doit()`` in inner products when they are
          encountered (default: True).
        * ``sum_doit``: call ``.doit()`` on sums when they are encountered
          (default: False). This is helpful for collapsing sums over Kronecker
          delta's that are created when calling ``qapply``.

    Returns
    =======

    e : Expr
        The original expression, but with the operators applied to states.

    Examples
    ========

        >>> from sympy.physics.quantum import qapply, Ket, Bra
        >>> b = Bra('b')
        >>> k = Ket('k')
        >>> A = k * b
        >>> A
        |k><b|
        >>> qapply(A * b.dual / (b * b.dual))
        |k>
        >>> qapply(k.dual * A / (k.dual * k))
        <b|
    """
    from sympy.physics.quantum.density import Density

    dagger = options.get('dagger', False)
    sum_doit = options.get('sum_doit', False)
    ip_doit = options.get('ip_doit', True)

    e = _sympify(e)

    # Using the kind API here helps us to narrow what types of expressions
    # we call ``ip_doit_func`` on.
    if e.kind == NumberKind:
        return ip_doit_func(e) if ip_doit else e

    # This may be a bit aggressive but ensures that everything gets expanded
    # to its simplest form before trying to apply operators. This includes
    # things like (A+B+C)*|a> and A*(|a>+|b>) and all Commutators and
    # TensorProducts. The only problem with this is that if we can't apply
    # all the Operators, we have just expanded everything.
    # TODO: don't expand the scalars in front of each Mul.
    e = e.expand(commutator=True, tensorproduct=True)

    # If we just have a raw ket, return it.
    if isinstance(e, KetBase):
        return e

    # We have an Add(a, b, c, ...) and compute
    # Add(qapply(a), qapply(b), ...)
    elif isinstance(e, Add):
        result = 0
        for arg in e.args:
            result += qapply(arg, **options)
        return result.expand()

    # For a Density operator call qapply on its state
    elif isinstance(e, Density):
        new_args = [(qapply(state, **options), prob) for (state,
                     prob) in e.args]
        return Density(*new_args)

    # For a raw TensorProduct, call qapply on its args.
    elif isinstance(e, TensorProduct):
        return TensorProduct(*[qapply(t, **options) for t in e.args])

    # For a Sum, call qapply on its function.
    elif isinstance(e, Sum):
        result = Sum(qapply(e.function, **options), *e.limits)
        result = sum_doit_func(result) if sum_doit else result
        return result

    # For a Pow, call qapply on its base.
    elif isinstance(e, Pow):
        return qapply(e.base, **options)**e.exp

    # We have a Mul where there might be actual operators to apply to kets.
    elif isinstance(e, Mul):
        c_part, nc_part = e.args_cnc()
        c_mul = Mul(*c_part)
        nc_mul = Mul(*nc_part)
        if not nc_part: # If we only have a commuting part, just return it.
            result = c_mul
        elif isinstance(nc_mul, Mul):
            result = c_mul*qapply_Mul(nc_mul, **options)
        else:
            result = c_mul*qapply(nc_mul, **options)
        if result == e and dagger:
            result = Dagger(qapply_Mul(Dagger(e), **options))
        result = ip_doit_func(result) if ip_doit else result
        result = sum_doit_func(result) if sum_doit else result
        return result

    # In all other cases (State, Operator, Pow, Commutator, InnerProduct,
    # OuterProduct) we won't ever have operators to apply to kets.
    else:
        return e

