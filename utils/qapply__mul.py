
def qapply_Mul(e, **options):

    args = list(e.args)
    extra = S.One
    result = None

    # If we only have 0 or 1 args, we have nothing to do and return.
    if len(args) <= 1 or not isinstance(e, Mul):
        return e
    rhs = args.pop()
    lhs = args.pop()

    # Make sure we have two non-commutative objects before proceeding.
    if (not isinstance(rhs, Wavefunction) and sympify(rhs).is_commutative) or \
            (not isinstance(lhs, Wavefunction) and sympify(lhs).is_commutative):
        return e

    # For a Pow with an integer exponent, apply one of them and reduce the
    # exponent by one.
    if isinstance(lhs, Pow) and lhs.exp.is_Integer:
        args.append(lhs.base**(lhs.exp - 1))
        lhs = lhs.base

    # Pull OuterProduct apart
    if isinstance(lhs, OuterProduct):
        args.append(lhs.ket)
        lhs = lhs.bra

    if isinstance(rhs, OuterProduct):
        extra = rhs.bra # Append to the right of the result
        rhs = rhs.ket

    # Call .doit() on Commutator/AntiCommutator.
    if isinstance(lhs, (Commutator, AntiCommutator)):
        comm = lhs.doit()
        if isinstance(comm, Add):
            return qapply(
                e.func(*(args + [comm.args[0], rhs])) +
                e.func(*(args + [comm.args[1], rhs])),
                **options
            )*extra
        else:
            return qapply(e.func(*args)*comm*rhs, **options)*extra

    # Apply tensor products of operators to states
    if isinstance(lhs, TensorProduct) and all(isinstance(arg, (Operator, State, Mul, Pow)) or arg == 1 for arg in lhs.args) and \
            isinstance(rhs, TensorProduct) and all(isinstance(arg, (Operator, State, Mul, Pow)) or arg == 1 for arg in rhs.args) and \
            len(lhs.args) == len(rhs.args):
        result = TensorProduct(*[qapply(lhs.args[n]*rhs.args[n], **options) for n in range(len(lhs.args))]).expand(tensorproduct=True)
        return qapply_Mul(e.func(*args), **options)*result*extra

    # For Sums, move the Sum to the right.
    if isinstance(rhs, Sum):
        if isinstance(lhs, Sum):
            if set(lhs.variables).intersection(set(rhs.variables)):
                raise ValueError('Duplicated dummy indices in separate sums in qapply.')
            limits = lhs.limits + rhs.limits
            result = Sum(qapply(lhs.function*rhs.function, **options), *limits)
            return qapply_Mul(e.func(*args)*result, **options)
        else:
            result = Sum(qapply(lhs*rhs.function, **options), *rhs.limits)
            return qapply_Mul(e.func(*args)*result, **options)

    if isinstance(lhs, Sum):
        result = Sum(qapply(lhs.function*rhs, **options), *lhs.limits)
        return qapply_Mul(e.func(*args)*result, **options)

    # Now try to actually apply the operator and build an inner product.
    _apply = getattr(lhs, '_apply_operator', None)
    if _apply is not None:
        try:
            result = _apply(rhs, **options)
        except NotImplementedError:
            result = None
    else:
        result = None

    if result is None:
        _apply_right = getattr(rhs, '_apply_from_right_to', None)
        if _apply_right is not None:
            try:
                result = _apply_right(lhs, **options)
            except NotImplementedError:
                result = None

    if result is None:
        if isinstance(lhs, BraBase) and isinstance(rhs, KetBase):
            result = InnerProduct(lhs, rhs)

    # TODO: I may need to expand before returning the final result.
    if isinstance(result, (int, complex, float)):
        return _sympify(result)
    elif result is None:
        if len(args) == 0:
            # We had two args to begin with so args=[].
            return e
        else:
            return qapply_Mul(e.func(*(args + [lhs])), **options)*rhs*extra
    elif isinstance(result, InnerProduct):
        return result*qapply_Mul(e.func(*args), **options)*extra
    else:  # result is a scalar times a Mul, Add or TensorProduct
        return qapply(e.func(*args)*result, **options)*extra

