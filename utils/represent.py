
def represent(expr, **options):
    """Represent the quantum expression in the given basis.

    In quantum mechanics abstract states and operators can be represented in
    various basis sets. Under this operation the follow transforms happen:

    * Ket -> column vector or function
    * Bra -> row vector of function
    * Operator -> matrix or differential operator

    This function is the top-level interface for this action.

    This function walks the SymPy expression tree looking for ``QExpr``
    instances that have a ``_represent`` method. This method is then called
    and the object is replaced by the representation returned by this method.
    By default, the ``_represent`` method will dispatch to other methods
    that handle the representation logic for a particular basis set. The
    naming convention for these methods is the following::

        def _represent_FooBasis(self, e, basis, **options)

    This function will have the logic for representing instances of its class
    in the basis set having a class named ``FooBasis``.

    Parameters
    ==========

    expr  : Expr
        The expression to represent.
    basis : Operator, basis set
        An object that contains the information about the basis set. If an
        operator is used, the basis is assumed to be the orthonormal
        eigenvectors of that operator. In general though, the basis argument
        can be any object that contains the basis set information.
    options : dict
        Key/value pairs of options that are passed to the underlying method
        that finds the representation. These options can be used to
        control how the representation is done. For example, this is where
        the size of the basis set would be set.

    Returns
    =======

    e : Expr
        The SymPy expression of the represented quantum expression.

    Examples
    ========

    Here we subclass ``Operator`` and ``Ket`` to create the z-spin operator
    and its spin 1/2 up eigenstate. By defining the ``_represent_SzOp``
    method, the ket can be represented in the z-spin basis.

    >>> from sympy.physics.quantum import Operator, represent, Ket
    >>> from sympy import Matrix

    >>> class SzUpKet(Ket):
    ...     def _represent_SzOp(self, basis, **options):
    ...         return Matrix([1,0])
    ...
    >>> class SzOp(Operator):
    ...     pass
    ...
    >>> sz = SzOp('Sz')
    >>> up = SzUpKet('up')
    >>> represent(up, basis=sz)
    Matrix([
    [1],
    [0]])

    Here we see an example of representations in a continuous
    basis. We see that the result of representing various combinations
    of cartesian position operators and kets give us continuous
    expressions involving DiracDelta functions.

    >>> from sympy.physics.quantum.cartesian import XOp, XKet, XBra
    >>> X = XOp()
    >>> x = XKet()
    >>> y = XBra('y')
    >>> represent(X*x)
    x*DiracDelta(x - x_2)
    """

    format = options.get('format', 'sympy')
    if format == 'numpy':
        import numpy as np
    if isinstance(expr, QExpr) and not isinstance(expr, OuterProduct):
        options['replace_none'] = False
        temp_basis = get_basis(expr, **options)
        if temp_basis is not None:
            options['basis'] = temp_basis
        try:
            return expr._represent(**options)
        except NotImplementedError as strerr:
            #If no _represent_FOO method exists, map to the
            #appropriate basis state and try
            #the other methods of representation
            options['replace_none'] = True

            if isinstance(expr, (KetBase, BraBase)):
                try:
                    return rep_innerproduct(expr, **options)
                except NotImplementedError:
                    raise NotImplementedError(strerr)
            elif isinstance(expr, Operator):
                try:
                    return rep_expectation(expr, **options)
                except NotImplementedError:
                    raise NotImplementedError(strerr)
            else:
                raise NotImplementedError(strerr)
    elif isinstance(expr, Add):
        result = represent(expr.args[0], **options)
        for args in expr.args[1:]:
            # scipy.sparse doesn't support += so we use plain = here.
            result = result + represent(args, **options)
        return result
    elif isinstance(expr, Pow):
        base, exp = expr.as_base_exp()
        if format in ('numpy', 'scipy.sparse'):
            exp = _sympy_to_scalar(exp)
        base = represent(base, **options)
        # scipy.sparse doesn't support negative exponents
        # and warns when inverting a matrix in csr format.
        if format == 'scipy.sparse' and exp < 0:
            from scipy.sparse.linalg import inv
            exp = - exp
            base = inv(base.tocsc()).tocsr()
        if format == 'numpy':
            return np.linalg.matrix_power(base, exp)
        return base ** exp
    elif isinstance(expr, TensorProduct):
        new_args = [represent(arg, **options) for arg in expr.args]
        return TensorProduct(*new_args)
    elif isinstance(expr, Dagger):
        return Dagger(represent(expr.args[0], **options))
    elif isinstance(expr, Commutator):
        A = expr.args[0]
        B = expr.args[1]
        return represent(Mul(A, B) - Mul(B, A), **options)
    elif isinstance(expr, AntiCommutator):
        A = expr.args[0]
        B = expr.args[1]
        return represent(Mul(A, B) + Mul(B, A), **options)
    elif not isinstance(expr, (Mul, OuterProduct, InnerProduct)):
        # We have removed special handling of inner products that used to be
        # required (before automatic transforms).
        # For numpy and scipy.sparse, we can only handle numerical prefactors.
        if format in ('numpy', 'scipy.sparse'):
            return _sympy_to_scalar(expr)
        return expr

    if not isinstance(expr, (Mul, OuterProduct, InnerProduct)):
        raise TypeError('Mul expected, got: %r' % expr)

    if "index" in options:
        options["index"] += 1
    else:
        options["index"] = 1

    if "unities" not in options:
        options["unities"] = []

    result = represent(expr.args[-1], **options)
    last_arg = expr.args[-1]

    for arg in reversed(expr.args[:-1]):
        if isinstance(last_arg, Operator):
            options["index"] += 1
            options["unities"].append(options["index"])
        elif isinstance(last_arg, BraBase) and isinstance(arg, KetBase):
            options["index"] += 1
        elif isinstance(last_arg, KetBase) and isinstance(arg, Operator):
            options["unities"].append(options["index"])
        elif isinstance(last_arg, KetBase) and isinstance(arg, BraBase):
            options["unities"].append(options["index"])

        next_arg = represent(arg, **options)
        if format == 'numpy' and isinstance(next_arg, np.ndarray):
            # Must use np.matmult to "matrix multiply" two np.ndarray
            result = np.matmul(next_arg, result)
        else:
            result = next_arg*result
        last_arg = arg

    # All three matrix formats create 1 by 1 matrices when inner products of
    # vectors are taken. In these cases, we simply return a scalar.
    result = flatten_scalar(result)

    result = integrate_result(expr, result, **options)

    return result

