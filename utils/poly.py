
def poly(expr, *gens, **args):
    """
    Efficiently transform an expression into a polynomial.

    Examples
    ========

    >>> from sympy import poly
    >>> from sympy.abc import x

    >>> poly(x*(x**2 + x - 1)**2)
    Poly(x**5 + 2*x**4 - x**3 - 2*x**2 + x, x, domain='ZZ')

    """
    options.allowed_flags(args, [])

    def _poly(expr, opt):
        terms, poly_terms = [], []

        for term in Add.make_args(expr):
            factors, poly_factors = [], []

            for factor in Mul.make_args(term):
                if factor.is_Add:
                    poly_factors.append(_poly(factor, opt))
                elif factor.is_Pow and factor.base.is_Add and \
                        factor.exp.is_Integer and factor.exp >= 0:
                    poly_factors.append(
                        _poly(factor.base, opt).pow(factor.exp))
                else:
                    factors.append(factor)

            if not poly_factors:
                terms.append(term)
            else:
                product = poly_factors[0]

                for factor in poly_factors[1:]:
                    product = product.mul(factor)

                if factors:
                    factor = Mul(*factors)

                    if factor.is_Number:
                        product *= factor
                    else:
                        product = product.mul(Poly._from_expr(factor, opt))

                poly_terms.append(product)

        if not poly_terms:
            result = Poly._from_expr(expr, opt)
        else:
            result = poly_terms[0]

            for term in poly_terms[1:]:
                result = result.add(term)

            if terms:
                term = Add(*terms)

                if term.is_Number:
                    result += term
                else:
                    result = result.add(Poly._from_expr(term, opt))

        return result.reorder(*opt.get('gens', ()), **args)

    expr = sympify(expr)

    if expr.is_Poly:
        return Poly(expr, *gens, **args)

    if 'expand' not in args:
        args['expand'] = False

    opt = options.build_options(gens, args)

    return _poly(expr, opt)


def poly(seq_of_zeros, *, xp):
    # Only reproduce the 1D variant of np.poly
    seq_of_zeros = xp.asarray(seq_of_zeros)
    seq_of_zeros = xpx.atleast_nd(seq_of_zeros, ndim=1, xp=xp)

    if seq_of_zeros.shape[0] == 0:
        return xp.asarray(1.0, dtype=xp.real(seq_of_zeros).dtype)

    # prefer np.convolve etc, if available
    convolve_func = getattr(xp, 'convolve', None)
    if convolve_func is None:
        from scipy.signal import convolve as convolve_func

    dt = seq_of_zeros.dtype
    a = xp.ones((1,), dtype=dt)
    one = xp.ones_like(seq_of_zeros[0])
    for zero in seq_of_zeros:
        a = convolve_func(a, xp.stack((one, -zero)), mode='full')

    if xp.isdtype(a.dtype, 'complex floating'):
        # if complex roots are all complex conjugates, the roots are real.
        roots = xp.asarray(seq_of_zeros, dtype=xp.complex128)
        if xp.all(xp.sort(xp.imag(roots)) == xp.sort(xp.imag(xp.conj(roots)))):
            a = xp.asarray(xp.real(a), copy=True)

    return a


def poly(seq_of_zeros):
    """
    Find the coefficients of a polynomial with the given sequence of roots.

    .. note::
       This forms part of the old polynomial API. Since version 1.4, the
       new polynomial API defined in `numpy.polynomial` is preferred.
       A summary of the differences can be found in the
       :doc:`transition guide </reference/routines.polynomials>`.

    Returns the coefficients of the polynomial whose leading coefficient
    is one for the given sequence of zeros (multiple roots must be included
    in the sequence as many times as their multiplicity; see Examples).
    A square matrix (or array, which will be treated as a matrix) can also
    be given, in which case the coefficients of the characteristic polynomial
    of the matrix are returned.

    Parameters
    ----------
    seq_of_zeros : array_like, shape (N,) or (N, N)
        A sequence of polynomial roots, or a square array or matrix object.

    Returns
    -------
    c : ndarray
        1D array of polynomial coefficients from highest to lowest degree:

        ``c[0] * x**(N) + c[1] * x**(N-1) + ... + c[N-1] * x + c[N]``
        where c[0] always equals 1.

    Raises
    ------
    ValueError
        If input is the wrong shape (the input must be a 1-D or square
        2-D array).

    See Also
    --------
    polyval : Compute polynomial values.
    roots : Return the roots of a polynomial.
    polyfit : Least squares polynomial fit.
    poly1d : A one-dimensional polynomial class.

    Notes
    -----
    Specifying the roots of a polynomial still leaves one degree of
    freedom, typically represented by an undetermined leading
    coefficient. [1]_ In the case of this function, that coefficient -
    the first one in the returned array - is always taken as one. (If
    for some reason you have one other point, the only automatic way
    presently to leverage that information is to use ``polyfit``.)

    The characteristic polynomial, :math:`p_a(t)`, of an `n`-by-`n`
    matrix **A** is given by

    :math:`p_a(t) = \\mathrm{det}(t\\, \\mathbf{I} - \\mathbf{A})`,

    where **I** is the `n`-by-`n` identity matrix. [2]_

    References
    ----------
    .. [1] M. Sullivan and M. Sullivan, III, "Algebra and Trigonometry,
       Enhanced With Graphing Utilities," Prentice-Hall, pg. 318, 1996.

    .. [2] G. Strang, "Linear Algebra and Its Applications, 2nd Edition,"
       Academic Press, pg. 182, 1980.

    Examples
    --------

    Given a sequence of a polynomial's zeros:

    >>> import numpy as np

    >>> np.poly((0, 0, 0)) # Multiple root example
    array([1., 0., 0., 0.])

    The line above represents z**3 + 0*z**2 + 0*z + 0.

    >>> np.poly((-1./2, 0, 1./2))
    array([ 1.  ,  0.  , -0.25,  0.  ])

    The line above represents z**3 - z/4

    >>> np.poly((np.random.random(1)[0], 0, np.random.random(1)[0]))
    array([ 1.        , -0.77086955,  0.08618131,  0.        ]) # random

    Given a square array object:

    >>> P = np.array([[0, 1./3], [-1./2, 0]])
    >>> np.poly(P)
    array([1.        , 0.        , 0.16666667])

    Note how in all cases the leading coefficient is always 1.

    """
    seq_of_zeros = atleast_1d(seq_of_zeros)
    sh = seq_of_zeros.shape

    if len(sh) == 2 and sh[0] == sh[1] and sh[0] != 0:
        seq_of_zeros = eigvals(seq_of_zeros)
    elif len(sh) == 1:
        dt = seq_of_zeros.dtype
        if dt.type is not NX.object_:
            seq_of_zeros = seq_of_zeros.astype(mintypecode(dt.char))
    else:
        raise ValueError("input must be 1d or non-empty square 2d array.")

    if len(seq_of_zeros) == 0:
        return 1.0
    dt = seq_of_zeros.dtype
    a = ones((1,), dtype=dt)
    for zero in seq_of_zeros:
        a = NX.convolve(a, array([1, -zero], dtype=dt), mode='full')

    if issubclass(a.dtype.type, NX.complexfloating):
        # if complex roots are all complex conjugates, the roots are real.
        roots = NX.asarray(seq_of_zeros, complex)
        if NX.all(NX.sort(roots) == NX.sort(roots.conjugate())):
            a = a.real.copy()

    return a


def Poly(request):
    return request.param


def poly(seq_of_zeros: ArrayLike) -> Array:
  r"""Returns the coefficients of a polynomial for the given sequence of roots.

  JAX implementation of :func:`numpy.poly`.

  Args:
    seq_of_zeros: A scalar or an array of roots of the polynomial of shape ``(M,)``
      or ``(M, M)``.

  Returns:
    An array containing the coefficients of the polynomial. The dtype of the
    output is always promoted to inexact.

  Note:

    :func:`jax.numpy.poly` differs from :func:`numpy.poly`:

    - When the input is a scalar, ``np.poly`` raises a ``TypeError``, whereas
      ``jnp.poly`` treats scalars the same as length-1 arrays.
    - For complex-valued or square-shaped inputs, ``jnp.poly`` always returns
      complex coefficients, whereas ``np.poly`` may return real or complex
      depending on their values.

  See also:
    - :func:`jax.numpy.polyfit`: Least squares polynomial fit.
    - :func:`jax.numpy.polyval`: Evaluate a polynomial at specific values.
    - :func:`jax.numpy.roots`: Computes the roots of a polynomial for given
      coefficients.

  Examples:

    Scalar inputs:

    >>> jnp.poly(1)
    Array([ 1., -1.], dtype=float32)

    Input array with integer values:

    >>> x = jnp.array([1, 2, 3])
    >>> jnp.poly(x)
    Array([ 1., -6., 11., -6.], dtype=float32)

    Input array with complex conjugates:

    >>> x = jnp.array([2, 1+2j, 1-2j])
    >>> jnp.poly(x)
    Array([  1.+0.j,  -4.+0.j,   9.+0.j, -10.+0.j], dtype=complex64)

    Input array as square matrix with real valued inputs:

    >>> x = jnp.array([[2, 1, 5],
    ...                [3, 4, 7],
    ...                [1, 3, 5]])
    >>> jnp.round(jnp.poly(x))
    Array([  1.+0.j, -11.-0.j,   9.+0.j, -15.+0.j], dtype=complex64)
  """
  seq_of_zeros = ensure_arraylike('poly', seq_of_zeros)
  seq_of_zeros, = promote_dtypes_inexact(seq_of_zeros)
  seq_of_zeros_arr = atleast_1d(seq_of_zeros)
  del seq_of_zeros

  sh = seq_of_zeros_arr.shape
  if len(sh) == 2 and sh[0] == sh[1] and sh[0] != 0:
    # import at runtime to avoid circular import
    from jax._src.numpy import linalg
    seq_of_zeros_arr = linalg.eigvals(seq_of_zeros_arr)

  if seq_of_zeros_arr.ndim != 1:
    raise ValueError("input must be 1d or non-empty square 2d array.")

  dt = seq_of_zeros_arr.dtype
  if len(seq_of_zeros_arr) == 0:
    return ones((), dtype=dt)

  a = ones((1,), dtype=dt)
  for k in range(len(seq_of_zeros_arr)):
    a = convolve(a, array([1, -seq_of_zeros_arr[k]], dtype=dt), mode='full')

  return a

