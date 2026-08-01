
def roots(f, *gens,
        auto=True,
        cubics=True,
        trig=False,
        quartics=True,
        quintics=False,
        multiple=False,
        filter=None,
        predicate=None,
        strict=False,
        **flags):
    """
    Computes symbolic roots of a univariate polynomial.

    Given a univariate polynomial f with symbolic coefficients (or
    a list of the polynomial's coefficients), returns a dictionary
    with its roots and their multiplicities.

    Only roots expressible via radicals will be returned.  To get
    a complete set of roots use RootOf class or numerical methods
    instead. By default cubic and quartic formulas are used in
    the algorithm. To disable them because of unreadable output
    set ``cubics=False`` or ``quartics=False`` respectively. If cubic
    roots are real but are expressed in terms of complex numbers
    (casus irreducibilis [1]) the ``trig`` flag can be set to True to
    have the solutions returned in terms of cosine and inverse cosine
    functions.

    To get roots from a specific domain set the ``filter`` flag with
    one of the following specifiers: Z, Q, R, I, C. By default all
    roots are returned (this is equivalent to setting ``filter='C'``).

    By default a dictionary is returned giving a compact result in
    case of multiple roots.  However to get a list containing all
    those roots set the ``multiple`` flag to True; the list will
    have identical roots appearing next to each other in the result.
    (For a given Poly, the all_roots method will give the roots in
    sorted numerical order.)

    If the ``strict`` flag is True, ``UnsolvableFactorError`` will be
    raised if the roots found are known to be incomplete (because
    some roots are not expressible in radicals).

    Examples
    ========

    >>> from sympy import Poly, roots, degree
    >>> from sympy.abc import x, y

    >>> roots(x**2 - 1, x)
    {-1: 1, 1: 1}

    >>> p = Poly(x**2-1, x)
    >>> roots(p)
    {-1: 1, 1: 1}

    >>> p = Poly(x**2-y, x, y)

    >>> roots(Poly(p, x))
    {-sqrt(y): 1, sqrt(y): 1}

    >>> roots(x**2 - y, x)
    {-sqrt(y): 1, sqrt(y): 1}

    >>> roots([1, 0, -1])
    {-1: 1, 1: 1}

    ``roots`` will only return roots expressible in radicals. If
    the given polynomial has some or all of its roots inexpressible in
    radicals, the result of ``roots`` will be incomplete or empty
    respectively.

    Example where result is incomplete:

    >>> roots((x-1)*(x**5-x+1), x)
    {1: 1}

    In this case, the polynomial has an unsolvable quintic factor
    whose roots cannot be expressed by radicals. The polynomial has a
    rational root (due to the factor `(x-1)`), which is returned since
    ``roots`` always finds all rational roots.

    Example where result is empty:

    >>> roots(x**7-3*x**2+1, x)
    {}

    Here, the polynomial has no roots expressible in radicals, so
    ``roots`` returns an empty dictionary.

    The result produced by ``roots`` is complete if and only if the
    sum of the multiplicity of each root is equal to the degree of
    the polynomial. If strict=True, UnsolvableFactorError will be
    raised if the result is incomplete.

    The result can be be checked for completeness as follows:

    >>> f = x**3-2*x**2+1
    >>> sum(roots(f, x).values()) == degree(f, x)
    True
    >>> f = (x-1)*(x**5-x+1)
    >>> sum(roots(f, x).values()) == degree(f, x)
    False


    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Cubic_equation#Trigonometric_and_hyperbolic_solutions

    """
    from sympy.polys.polytools import to_rational_coeffs
    flags = dict(flags)

    if isinstance(f, list):
        if gens:
            raise ValueError('redundant generators given')

        x = Dummy('x')

        poly, i = {}, len(f) - 1

        for coeff in f:
            poly[i], i = sympify(coeff), i - 1

        f = Poly(poly, x, field=True)
    else:
        try:
            F = Poly(f, *gens, **flags)
            if not isinstance(f, Poly) and not F.gen.is_Symbol:
                raise PolynomialError("generator must be a Symbol")
            f = F
        except GeneratorsNeeded:
            if multiple:
                return []
            else:
                return {}
        else:
            n = f.degree()
            if f.length() == 2 and n > 2:
                # check for foo**n in constant if dep is c*gen**m
                con, dep = f.as_expr().as_independent(*f.gens)
                fcon = -(-con).factor()
                if fcon != con:
                    con = fcon
                    bases = []
                    for i in Mul.make_args(con):
                        if i.is_Pow:
                            b, e = i.as_base_exp()
                            if e.is_Integer and b.is_Add:
                                bases.append((b, Dummy(positive=True)))
                    if bases:
                        rv = roots(Poly((dep + con).xreplace(dict(bases)),
                            *f.gens), *F.gens,
                            auto=auto,
                            cubics=cubics,
                            trig=trig,
                            quartics=quartics,
                            quintics=quintics,
                            multiple=multiple,
                            filter=filter,
                            predicate=predicate,
                            **flags)
                        return {factor_terms(k.xreplace(
                            {v: k for k, v in bases})
                        ): v for k, v in rv.items()}

        if f.is_multivariate:
            raise PolynomialError('multivariate polynomials are not supported')

    def _update_dict(result, zeros, currentroot, k):
        if currentroot == S.Zero:
            if S.Zero in zeros:
                zeros[S.Zero] += k
            else:
                zeros[S.Zero] = k
        if currentroot in result:
            result[currentroot] += k
        else:
            result[currentroot] = k

    def _try_decompose(f):
        """Find roots using functional decomposition. """
        factors, roots = f.decompose(), []

        for currentroot in _try_heuristics(factors[0]):
            roots.append(currentroot)

        for currentfactor in factors[1:]:
            previous, roots = list(roots), []

            for currentroot in previous:
                g = currentfactor - Poly(currentroot, f.gen)

                for currentroot in _try_heuristics(g):
                    roots.append(currentroot)

        return roots

    def _try_heuristics(f):
        """Find roots using formulas and some tricks. """
        if f.is_ground:
            return []
        if f.is_monomial:
            return [S.Zero]*f.degree()

        if f.length() == 2:
            if f.degree() == 1:
                return list(map(cancel, roots_linear(f)))
            else:
                return roots_binomial(f)

        result = []

        for i in [-1, 1]:
            if not f.eval(i):
                f = f.quo(Poly(f.gen - i, f.gen))
                result.append(i)
                break

        n = f.degree()

        if n == 1:
            result += list(map(cancel, roots_linear(f)))
        elif n == 2:
            result += list(map(cancel, roots_quadratic(f)))
        elif f.is_cyclotomic:
            result += roots_cyclotomic(f)
        elif n == 3 and cubics:
            result += roots_cubic(f, trig=trig)
        elif n == 4 and quartics:
            result += roots_quartic(f)
        elif n == 5 and quintics:
            result += roots_quintic(f)

        return result

    # Convert the generators to symbols
    dumgens = symbols('x:%d' % len(f.gens), cls=Dummy)
    f = f.per(f.rep, dumgens)

    (k,), f = f.terms_gcd()

    if not k:
        zeros = {}
    else:
        zeros = {S.Zero: k}

    coeff, f = preprocess_roots(f)

    if auto and f.get_domain().is_Ring:
        f = f.to_field()

    # Use EX instead of ZZ_I or QQ_I
    if f.get_domain().is_QQ_I:
        f = f.per(f.rep.convert(EX))

    rescale_x = None
    translate_x = None

    result = {}

    if not f.is_ground:
        dom = f.get_domain()
        if not dom.is_Exact and dom.is_Numerical:
            for r in f.nroots():
                _update_dict(result, zeros, r, 1)
        elif f.degree() == 1:
            _update_dict(result, zeros, roots_linear(f)[0], 1)
        elif f.length() == 2:
            roots_fun = roots_quadratic if f.degree() == 2 else roots_binomial
            for r in roots_fun(f):
                _update_dict(result, zeros, r, 1)
        else:
            _, factors = Poly(f.as_expr()).factor_list()
            if len(factors) == 1 and f.degree() == 2:
                for r in roots_quadratic(f):
                    _update_dict(result, zeros, r, 1)
            else:
                if len(factors) == 1 and factors[0][1] == 1:
                    if f.get_domain().is_EX:
                        res = to_rational_coeffs(f)
                        if res:
                            if res[0] is None:
                                translate_x, f = res[2:]
                            else:
                                rescale_x, f = res[1], res[-1]
                            result = roots(f)
                            if not result:
                                for currentroot in _try_decompose(f):
                                    _update_dict(result, zeros, currentroot, 1)
                        else:
                            for r in _try_heuristics(f):
                                _update_dict(result, zeros, r, 1)
                    else:
                        for currentroot in _try_decompose(f):
                            _update_dict(result, zeros, currentroot, 1)
                else:
                    for currentfactor, k in factors:
                        for r in _try_heuristics(Poly(currentfactor, f.gen, field=True)):
                            _update_dict(result, zeros, r, k)

    if coeff is not S.One:
        _result, result, = result, {}

        for currentroot, k in _result.items():
            result[coeff*currentroot] = k

    if filter not in [None, 'C']:
        handlers = {
            'Z': lambda r: r.is_Integer,
            'Q': lambda r: r.is_Rational,
            'R': lambda r: all(a.is_real for a in r.as_numer_denom()),
            'I': lambda r: r.is_imaginary,
        }

        try:
            query = handlers[filter]
        except KeyError:
            raise ValueError("Invalid filter: %s" % filter)

        for zero in dict(result).keys():
            if not query(zero):
                del result[zero]

    if predicate is not None:
        for zero in dict(result).keys():
            if not predicate(zero):
                del result[zero]
    if rescale_x:
        result1 = {}
        for k, v in result.items():
            result1[k*rescale_x] = v
        result = result1
    if translate_x:
        result1 = {}
        for k, v in result.items():
            result1[k + translate_x] = v
        result = result1

    # adding zero roots after non-trivial roots have been translated
    result.update(zeros)

    if strict and sum(result.values()) < f.degree():
        raise UnsolvableFactorError(filldedent('''
            Strict mode: some factors cannot be solved in radicals, so
            a complete list of solutions cannot be returned. Call
            roots with strict=False to get solutions expressible in
            radicals (if there are any).
            '''))

    if not multiple:
        return result
    else:
        zeros = []

        for zero in ordered(result):
            zeros.extend([zero]*result[zero])

        return zeros


def roots(p):
    """
    Return the roots of a polynomial with coefficients given in p.

    .. note::
       This forms part of the old polynomial API. Since version 1.4, the
       new polynomial API defined in `numpy.polynomial` is preferred.
       A summary of the differences can be found in the
       :doc:`transition guide </reference/routines.polynomials>`.

    The values in the rank-1 array `p` are coefficients of a polynomial.
    If the length of `p` is n+1 then the polynomial is described by::

      p[0] * x**n + p[1] * x**(n-1) + ... + p[n-1]*x + p[n]

    Parameters
    ----------
    p : array_like
        Rank-1 array of polynomial coefficients.

    Returns
    -------
    out : ndarray
        An array containing the roots of the polynomial.

    Raises
    ------
    ValueError
        When `p` cannot be converted to a rank-1 array.

    See also
    --------
    poly : Find the coefficients of a polynomial with a given sequence
           of roots.
    polyval : Compute polynomial values.
    polyfit : Least squares polynomial fit.
    poly1d : A one-dimensional polynomial class.

    Notes
    -----
    The algorithm relies on computing the eigenvalues of the
    companion matrix [1]_.

    References
    ----------
    .. [1] R. A. Horn & C. R. Johnson, *Matrix Analysis*.  Cambridge, UK:
        Cambridge University Press, 1999, pp. 146-7.

    Examples
    --------
    >>> import numpy as np
    >>> coeff = [3.2, 2, 1]
    >>> np.roots(coeff)
    array([-0.3125+0.46351241j, -0.3125-0.46351241j])

    """
    # If input is scalar, this makes it an array
    p = atleast_1d(p)
    if p.ndim != 1:
        raise ValueError("Input must be a rank-1 array.")

    # find non-zero array entries
    non_zero = NX.nonzero(NX.ravel(p))[0]

    # Return an empty array if polynomial is all zeros
    if len(non_zero) == 0:
        return NX.array([])

    # find the number of trailing zeros -- this is the number of roots at 0.
    trailing_zeros = len(p) - non_zero[-1] - 1

    # strip leading and trailing zeros
    p = p[int(non_zero[0]):int(non_zero[-1]) + 1]

    # casting: if incoming array isn't floating point, make it floating point.
    if not issubclass(p.dtype.type, (NX.floating, NX.complexfloating)):
        p = p.astype(float)

    N = len(p)
    if N > 1:
        # build companion matrix and find its eigenvalues (the roots)
        A = diag(NX.ones((N - 2,), p.dtype), -1)
        A[0, :] = -p[1:] / p[0]
        roots = eigvals(A)

        # backwards compat: return real values if possible
        from numpy.linalg._linalg import _to_real_if_imag_zero
        roots = _to_real_if_imag_zero(roots, A)
    else:
        roots = NX.array([])

    # tack any zeros onto the back of the array
    roots = hstack((roots, NX.zeros(trailing_zeros, roots.dtype)))
    return roots


def roots(p: ArrayLike, *, strip_zeros: bool = True) -> Array:
  r"""Returns the roots of a polynomial given the coefficients ``p``.

  JAX implementations of :func:`numpy.roots`.

  Args:
    p: Array of polynomial coefficients having rank-1.
    strip_zeros : bool, default=True. If True, then leading zeros in the
      coefficients will be stripped, similar to :func:`numpy.roots`. If set to
      False, leading zeros will not be stripped, and undefined roots will be
      represented by NaN values in the function output. ``strip_zeros`` must be
      set to ``False`` for the function to be compatible with :func:`jax.jit` and
      other JAX transformations.

  Returns:
    An array containing the roots of the polynomial.

  Note:
    Unlike ``np.roots`` of this function, the ``jnp.roots`` returns the roots
    in a complex array regardless of the values of the roots.

  See Also:
    - :func:`jax.numpy.poly`: Finds the polynomial coefficients of the given
      sequence of roots.
    - :func:`jax.numpy.polyfit`: Least squares polynomial fit to data.
    - :func:`jax.numpy.polyval`: Evaluate a polynomial at specific values.

  Examples:
    >>> coeffs = jnp.array([0, 1, 2])

    The default behavior matches numpy and strips leading zeros:

    >>> jnp.roots(coeffs)
    Array([-2.+0.j], dtype=complex64)

    With ``strip_zeros=False``, extra roots are set to NaN:

    >>> jnp.roots(coeffs, strip_zeros=False)
    Array([-2. +0.j, nan+nanj], dtype=complex64)
  """
  p = ensure_arraylike("roots", p)
  p, = promote_dtypes_inexact(p)
  p_arr = atleast_1d(p)
  del p
  if p_arr.ndim != 1:
    raise ValueError("Input must be a rank-1 array.")
  if p_arr.size < 2:
    return array([], dtype=dtypes.to_complex_dtype(p_arr.dtype))
  num_leading_zeros = _where(all(p_arr == 0), len(p_arr), argmin(p_arr == 0))

  if strip_zeros:
    num_leading_zeros = core.concrete_or_error(int, num_leading_zeros,
      "The error occurred in the jnp.roots() function. To use this within a "
      "JIT-compiled context, pass strip_zeros=False, but be aware that leading zeros "
      "will result in some returned roots being set to NaN.")
    return _roots_no_zeros(p_arr[num_leading_zeros:])
  else:
    return _roots_with_zeros(p_arr, num_leading_zeros)

