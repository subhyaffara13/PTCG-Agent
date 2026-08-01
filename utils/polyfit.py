
def polyfit(x, y, deg, *, xp, rcond=None):
    # only reproduce the variant with full=False, w=None, cov=False
    order = int(deg) + 1
    x = xp.asarray(x)
    y = xp.asarray(y)
    x, y = xp_promote(x, y, force_floating=True, xp=xp)

    # check arguments.
    if deg < 0:
        raise ValueError("expected deg >= 0")
    if x.ndim != 1:
        raise TypeError("expected 1D vector for x")
    if xp_size(x) == 0:
        raise TypeError("expected non-empty vector for x")
    if y.ndim < 1 or y.ndim > 2:
        raise TypeError("expected 1D or 2D array for y")
    if x.shape[0] != y.shape[0]:
        raise TypeError("expected x and y to have same length")

    # set rcond
    if rcond is None:
        rcond = x.shape[0] * xp.finfo(x.dtype).eps

    # set up least squares equation for powers of x: lhs = vander(x, order)
    powers = xp.flip(xp.arange(order, dtype=x.dtype, device=xp_device(x)))
    lhs = x[:, None] ** powers[None, :]

    # scale lhs to improve condition number and solve
    scale = xp.sqrt(xp.sum(lhs * lhs, axis=0))
    lhs /= scale

    c, _, rank, _ = _lstsq(lhs, y, rcond=rcond, xp=xp)
    c = (c.T / scale).T  # broadcast scale coefficients

    # warn on rank reduction, which indicates an ill conditioned matrix
    if rank != order:
        msg = "Polyfit may be poorly conditioned"
        warnings.warn(msg, RankWarning, stacklevel=2)

    return c


def polyfit(x, y, deg, rcond=None, full=False, w=None, cov=False):
    """
    Least squares polynomial fit.

    .. note::
       This forms part of the old polynomial API. Since version 1.4, the
       new polynomial API defined in `numpy.polynomial` is preferred.
       A summary of the differences can be found in the
       :doc:`transition guide </reference/routines.polynomials>`.

    Fit a polynomial ``p[0] * x**deg + ... + p[deg]`` of degree `deg`
    to points `(x, y)`. Returns a vector of coefficients `p` that minimises
    the squared error in the order `deg`, `deg-1`, ... `0`.

    The `Polynomial.fit <numpy.polynomial.polynomial.Polynomial.fit>` class
    method is recommended for new code as it is more stable numerically. See
    the documentation of the method for more information.

    Parameters
    ----------
    x : array_like, shape (M,)
        x-coordinates of the M sample points ``(x[i], y[i])``.
    y : array_like, shape (M,) or (M, K)
        y-coordinates of the sample points. Several data sets of sample
        points sharing the same x-coordinates can be fitted at once by
        passing in a 2D-array that contains one dataset per column.
    deg : int
        Degree of the fitting polynomial
    rcond : float, optional
        Relative condition number of the fit. Singular values smaller than
        this relative to the largest singular value will be ignored. The
        default value is len(x)*eps, where eps is the relative precision of
        the float type, about 2e-16 in most cases.
    full : bool, optional
        Switch determining nature of return value. When it is False (the
        default) just the coefficients are returned, when True diagnostic
        information from the singular value decomposition is also returned.
    w : array_like, shape (M,), optional
        Weights. If not None, the weight ``w[i]`` applies to the unsquared
        residual ``y[i] - y_hat[i]`` at ``x[i]``. Ideally the weights are
        chosen so that the errors of the products ``w[i]*y[i]`` all have the
        same variance.  When using inverse-variance weighting, use
        ``w[i] = 1/sigma(y[i])``.  The default value is None.
    cov : bool or str, optional
        If given and not `False`, return not just the estimate but also its
        covariance matrix. By default, the covariance are scaled by
        chi2/dof, where dof = M - (deg + 1), i.e., the weights are presumed
        to be unreliable except in a relative sense and everything is scaled
        such that the reduced chi2 is unity. This scaling is omitted if
        ``cov='unscaled'``, as is relevant for the case that the weights are
        w = 1/sigma, with sigma known to be a reliable estimate of the
        uncertainty.

    Returns
    -------
    p : ndarray, shape (deg + 1,) or (deg + 1, K)
        Polynomial coefficients, highest power first.  If `y` was 2-D, the
        coefficients for `k`-th data set are in ``p[:,k]``.

    residuals, rank, singular_values, rcond
        These values are only returned if ``full == True``

        - residuals -- sum of squared residuals of the least squares fit
        - rank -- the effective rank of the scaled Vandermonde
          coefficient matrix
        - singular_values -- singular values of the scaled Vandermonde
          coefficient matrix
        - rcond -- value of `rcond`.

        For more details, see `numpy.linalg.lstsq`.

    V : ndarray, shape (deg + 1, deg + 1) or (deg + 1, deg + 1, K)
        Present only if ``full == False`` and ``cov == True``.  The covariance
        matrix of the polynomial coefficient estimates.  The diagonal of
        this matrix are the variance estimates for each coefficient.  If y
        is a 2-D array, then the covariance matrix for the `k`-th data set
        are in ``V[:,:,k]``


    Warns
    -----
    RankWarning
        The rank of the coefficient matrix in the least-squares fit is
        deficient. The warning is only raised if ``full == False``.

        The warnings can be turned off by

        >>> import warnings
        >>> warnings.simplefilter('ignore', np.exceptions.RankWarning)

    See Also
    --------
    polyval : Compute polynomial values.
    linalg.lstsq : Computes a least-squares fit.
    scipy.interpolate.UnivariateSpline : Computes spline fits.

    Notes
    -----
    The solution minimizes the squared error

    .. math::
        E = \\sum_{j=0}^k |p(x_j) - y_j|^2

    in the equations::

        x[0]**n * p[0] + ... + x[0] * p[n-1] + p[n] = y[0]
        x[1]**n * p[0] + ... + x[1] * p[n-1] + p[n] = y[1]
        ...
        x[k]**n * p[0] + ... + x[k] * p[n-1] + p[n] = y[k]

    The coefficient matrix of the coefficients `p` is a Vandermonde matrix.

    `polyfit` issues a `~exceptions.RankWarning` when the least-squares fit is
    badly conditioned. This implies that the best fit is not well-defined due
    to numerical error. The results may be improved by lowering the polynomial
    degree or by replacing `x` by `x` - `x`.mean(). The `rcond` parameter
    can also be set to a value smaller than its default, but the resulting
    fit may be spurious: including contributions from the small singular
    values can add numerical noise to the result.

    Note that fitting polynomial coefficients is inherently badly conditioned
    when the degree of the polynomial is large or the interval of sample points
    is badly centered. The quality of the fit should always be checked in these
    cases. When polynomial fits are not satisfactory, splines may be a good
    alternative.

    References
    ----------
    .. [1] Wikipedia, "Curve fitting",
           https://en.wikipedia.org/wiki/Curve_fitting
    .. [2] Wikipedia, "Polynomial interpolation",
           https://en.wikipedia.org/wiki/Polynomial_interpolation

    Examples
    --------
    >>> import numpy as np
    >>> import warnings
    >>> x = np.array([0.0, 1.0, 2.0, 3.0,  4.0,  5.0])
    >>> y = np.array([0.0, 0.8, 0.9, 0.1, -0.8, -1.0])
    >>> z = np.polyfit(x, y, 3)
    >>> z
    array([ 0.08703704, -0.81349206,  1.69312169, -0.03968254]) # may vary

    It is convenient to use `poly1d` objects for dealing with polynomials:

    >>> p = np.poly1d(z)
    >>> p(0.5)
    0.6143849206349179 # may vary
    >>> p(3.5)
    -0.34732142857143039 # may vary
    >>> p(10)
    22.579365079365115 # may vary

    High-order polynomials may oscillate wildly:

    >>> with warnings.catch_warnings():
    ...     warnings.simplefilter('ignore', np.exceptions.RankWarning)
    ...     p30 = np.poly1d(np.polyfit(x, y, 30))
    ...
    >>> p30(4)
    -0.80000000000000204 # may vary
    >>> p30(5)
    -0.99999999999999445 # may vary
    >>> p30(4.5)
    -0.10547061179440398 # may vary

    Illustration:

    >>> import matplotlib.pyplot as plt
    >>> xp = np.linspace(-2, 6, 100)
    >>> _ = plt.plot(x, y, '.', xp, p(xp), '-', xp, p30(xp), '--')
    >>> plt.ylim(-2,2)
    (-2, 2)
    >>> plt.show()

    """
    order = int(deg) + 1
    x = NX.asarray(x) + 0.0
    y = NX.asarray(y) + 0.0

    # check arguments.
    if deg < 0:
        raise ValueError("expected deg >= 0")
    if x.ndim != 1:
        raise TypeError("expected 1D vector for x")
    if x.size == 0:
        raise TypeError("expected non-empty vector for x")
    if y.ndim < 1 or y.ndim > 2:
        raise TypeError("expected 1D or 2D array for y")
    if x.shape[0] != y.shape[0]:
        raise TypeError("expected x and y to have same length")

    # set rcond
    if rcond is None:
        rcond = len(x) * finfo(x.dtype).eps

    # set up least squares equation for powers of x
    lhs = vander(x, order)
    rhs = y

    # apply weighting
    if w is not None:
        w = NX.asarray(w) + 0.0
        if w.ndim != 1:
            raise TypeError("expected a 1-d array for weights")
        if w.shape[0] != y.shape[0]:
            raise TypeError("expected w and y to have the same length")
        lhs *= w[:, NX.newaxis]
        if rhs.ndim == 2:
            rhs *= w[:, NX.newaxis]
        else:
            rhs *= w

    # scale lhs to improve condition number and solve
    scale = NX.sqrt((lhs * lhs).sum(axis=0))
    lhs /= scale
    c, resids, rank, s = lstsq(lhs, rhs, rcond)
    c = (c.T / scale).T  # broadcast scale coefficients

    # warn on rank reduction, which indicates an ill conditioned matrix
    if rank != order and not full:
        msg = "Polyfit may be poorly conditioned"
        warnings.warn(msg, RankWarning, stacklevel=2)

    if full:
        return c, resids, rank, s, rcond
    elif cov:
        Vbase = inv(dot(lhs.T, lhs))
        Vbase /= NX.outer(scale, scale)
        if cov == "unscaled":
            fac = 1
        else:
            if len(x) <= order:
                raise ValueError("the number of data points must exceed order "
                                 "to scale the covariance matrix")
            # note, this used to be: fac = resids / (len(x) - order - 2.0)
            # it was decided that the "- 2" (originally justified by "Bayesian
            # uncertainty analysis") is not what the user expects
            # (see gh-11196 and gh-11197)
            fac = resids / (len(x) - order)
        if y.ndim == 1:
            return c, Vbase * fac
        else:
            return c, Vbase[:, :, NX.newaxis] * fac
    else:
        return c


def polyfit(x, y, deg, rcond=None, full=False, w=None, cov=False):
    """
    Any masked values in x is propagated in y, and vice-versa.

    """
    x = asarray(x)
    y = asarray(y)

    m = getmask(x)
    if y.ndim == 1:
        m = mask_or(m, getmask(y))
    elif y.ndim == 2:
        my = getmask(mask_rows(y))
        if my is not nomask:
            m = mask_or(m, my[:, 0])
    else:
        raise TypeError("Expected a 1D or 2D array for y!")

    if w is not None:
        w = asarray(w)
        if w.ndim != 1:
            raise TypeError("expected a 1-d array for weights")
        if w.shape[0] != y.shape[0]:
            raise TypeError("expected w and y to have the same length")
        m = mask_or(m, getmask(w))

    if m is not nomask:
        not_m = ~m
        if w is not None:
            w = w[not_m]
        return np.polyfit(x[not_m], y[not_m], deg, rcond, full, w, cov)
    else:
        return np.polyfit(x, y, deg, rcond, full, w, cov)


def polyfit(x, y, deg, rcond=None, full=False, w=None):
    """
    Least-squares fit of a polynomial to data.

    Return the coefficients of a polynomial of degree `deg` that is the
    least squares fit to the data values `y` given at points `x`. If `y` is
    1-D the returned coefficients will also be 1-D. If `y` is 2-D multiple
    fits are done, one for each column of `y`, and the resulting
    coefficients are stored in the corresponding columns of a 2-D return.
    The fitted polynomial(s) are in the form

    .. math::  p(x) = c_0 + c_1 * x + ... + c_n * x^n,

    where `n` is `deg`.

    Parameters
    ----------
    x : array_like, shape (`M`,)
        x-coordinates of the `M` sample (data) points ``(x[i], y[i])``.
    y : array_like, shape (`M`,) or (`M`, `K`)
        y-coordinates of the sample points.  Several sets of sample points
        sharing the same x-coordinates can be (independently) fit with one
        call to `polyfit` by passing in for `y` a 2-D array that contains
        one data set per column.
    deg : int or 1-D array_like
        Degree(s) of the fitting polynomials. If `deg` is a single integer
        all terms up to and including the `deg`'th term are included in the
        fit. For NumPy versions >= 1.11.0 a list of integers specifying the
        degrees of the terms to include may be used instead.
    rcond : float, optional
        Relative condition number of the fit.  Singular values smaller
        than `rcond`, relative to the largest singular value, will be
        ignored.  The default value is ``len(x)*eps``, where `eps` is the
        relative precision of the platform's float type, about 2e-16 in
        most cases.
    full : bool, optional
        Switch determining the nature of the return value.  When ``False``
        (the default) just the coefficients are returned; when ``True``,
        diagnostic information from the singular value decomposition (used
        to solve the fit's matrix equation) is also returned.
    w : array_like, shape (`M`,), optional
        Weights. If not None, the weight ``w[i]`` applies to the unsquared
        residual ``y[i] - y_hat[i]`` at ``x[i]``. Ideally the weights are
        chosen so that the errors of the products ``w[i]*y[i]`` all have the
        same variance.  When using inverse-variance weighting, use
        ``w[i] = 1/sigma(y[i])``.  The default value is None.

    Returns
    -------
    coef : ndarray, shape (`deg` + 1,) or (`deg` + 1, `K`)
        Polynomial coefficients ordered from low to high.  If `y` was 2-D,
        the coefficients in column `k` of `coef` represent the polynomial
        fit to the data in `y`'s `k`-th column.

    [residuals, rank, singular_values, rcond] : list
        These values are only returned if ``full == True``

        - residuals -- sum of squared residuals of the least squares fit
        - rank -- the numerical rank of the scaled Vandermonde matrix
        - singular_values -- singular values of the scaled Vandermonde matrix
        - rcond -- value of `rcond`.

        For more details, see `numpy.linalg.lstsq`.

    Raises
    ------
    RankWarning
        Raised if the matrix in the least-squares fit is rank deficient.
        The warning is only raised if ``full == False``.  The warnings can
        be turned off by:

        >>> import warnings
        >>> warnings.simplefilter('ignore', np.exceptions.RankWarning)

    See Also
    --------
    numpy.polynomial.chebyshev.chebfit
    numpy.polynomial.legendre.legfit
    numpy.polynomial.laguerre.lagfit
    numpy.polynomial.hermite.hermfit
    numpy.polynomial.hermite_e.hermefit
    polyval : Evaluates a polynomial.
    polyvander : Vandermonde matrix for powers.
    numpy.linalg.lstsq : Computes a least-squares fit from the matrix.
    scipy.interpolate.UnivariateSpline : Computes spline fits.

    Notes
    -----
    The solution is the coefficients of the polynomial `p` that minimizes
    the sum of the weighted squared errors

    .. math:: E = \\sum_j w_j^2 * |y_j - p(x_j)|^2,

    where the :math:`w_j` are the weights. This problem is solved by
    setting up the (typically) over-determined matrix equation:

    .. math:: V(x) * c = w * y,

    where `V` is the weighted pseudo Vandermonde matrix of `x`, `c` are the
    coefficients to be solved for, `w` are the weights, and `y` are the
    observed values.  This equation is then solved using the singular value
    decomposition of `V`.

    If some of the singular values of `V` are so small that they are
    neglected (and `full` == ``False``), a `~exceptions.RankWarning` will be
    raised.  This means that the coefficient values may be poorly determined.
    Fitting to a lower order polynomial will usually get rid of the warning
    (but may not be what you want, of course; if you have independent
    reason(s) for choosing the degree which isn't working, you may have to:
    a) reconsider those reasons, and/or b) reconsider the quality of your
    data).  The `rcond` parameter can also be set to a value smaller than
    its default, but the resulting fit may be spurious and have large
    contributions from roundoff error.

    Polynomial fits using double precision tend to "fail" at about
    (polynomial) degree 20. Fits using Chebyshev or Legendre series are
    generally better conditioned, but much can still depend on the
    distribution of the sample points and the smoothness of the data.  If
    the quality of the fit is inadequate, splines may be a good
    alternative.

    Examples
    --------
    >>> import numpy as np
    >>> from numpy.polynomial import polynomial as P
    >>> x = np.linspace(-1,1,51)  # x "data": [-1, -0.96, ..., 0.96, 1]
    >>> rng = np.random.default_rng()
    >>> err = rng.normal(size=len(x))
    >>> y = x**3 - x + err  # x^3 - x + Gaussian noise
    >>> c, stats = P.polyfit(x,y,3,full=True)
    >>> c # c[0], c[1] approx. -1, c[2] should be approx. 0, c[3] approx. 1
    array([ 0.23111996, -1.02785049, -0.2241444 ,  1.08405657]) # may vary
    >>> stats # note the large SSR, explaining the rather poor results
    [array([48.312088]),                                        # may vary
     4,
     array([1.38446749, 1.32119158, 0.50443316, 0.28853036]),
     1.1324274851176597e-14]

    Same thing without the added noise

    >>> y = x**3 - x
    >>> c, stats = P.polyfit(x,y,3,full=True)
    >>> c # c[0], c[1] ~= -1, c[2] should be "very close to 0", c[3] ~= 1
    array([-6.73496154e-17, -1.00000000e+00,  0.00000000e+00,  1.00000000e+00])
    >>> stats # note the minuscule SSR
    [array([8.79579319e-31]),
     np.int32(4),
     array([1.38446749, 1.32119158, 0.50443316, 0.28853036]),
     1.1324274851176597e-14]

    """
    return pu._fit(polyvander, x, y, deg, rcond, full, w)


def polyfit(x: ArrayLike, y: ArrayLike, deg: int, rcond: float | None = None,
            full: bool = False, w: ArrayLike | None = None, cov: bool = False
            ) -> Array | tuple[Array, ...]:
  r"""Least squares polynomial fit to data.

  Jax implementation of :func:`numpy.polyfit`.

  Given a set of data points ``(x, y)`` and degree of polynomial ``deg``, the
  function finds a polynomial equation of the form:

  .. math::

    y = p(x) = p[0] x^{deg} + p[1] x^{deg - 1} + ... + p[deg]

  Args:
    x: Array of data points of shape ``(M,)``.
    y: Array of data points of shape ``(M,)`` or ``(M, K)``.
    deg: Degree of the polynomials. It must be specified statically.
    rcond: Relative condition number of the fit. Default value is ``len(x) * eps``.
       It must be specified statically.
    full: Switch that controls the return value. Default is ``False`` which
      restricts the return value to the array of polynomial coefficients ``p``.
      If ``True``, the function returns a tuple ``(p, resids, rank, s, rcond)``.
      It must be specified statically.
    w: Array of weights of shape ``(M,)``. If None, all data points are considered
      to have equal weight. If not None, the weight :math:`w_i` is applied to the
      unsquared residual of :math:`y_i - \widehat{y}_i` at :math:`x_i`, where
      :math:`\widehat{y}_i` is the fitted value of :math:`y_i`. Default is None.
    cov: Boolean or string. If ``True``, returns the covariance matrix scaled
      by ``resids/(M-deg-1)`` along with polynomial coefficients. If
      ``cov='unscaled'``, returns the unscaled version of covariance matrix.
      Default is ``False``. ``cov`` is ignored if ``full=True``. It must be
      specified statically.

  Returns:
    - An array polynomial coefficients ``p`` if ``full=False`` and ``cov=False``.

    - A tuple of arrays ``(p, resids, rank, s, rcond)`` if ``full=True``. Where

      - ``p`` is an array of shape ``(M,)`` or ``(M, K)`` containing the polynomial
        coefficients.
      - ``resids`` is the sum of squared residual of shape () or (K,).
      - ``rank`` is the rank of the matrix ``x``.
      - ``s`` is the singular values of the matrix ``x``.
      - ``rcond`` as the array.
    - A tuple of arrays ``(p, C)`` if ``full=False`` and ``cov=True``. Where

      - ``p`` is an array of shape ``(M,)`` or ``(M, K)`` containing the polynomial
        coefficients.
      - ``C`` is the covariance matrix of polynomial coefficients of shape
        ``(deg + 1, deg + 1)`` or ``(deg + 1, deg + 1, 1)``.

  Note:
    Unlike :func:`numpy.polyfit` implementation of polyfit, :func:`jax.numpy.polyfit`
    will not warn on rank reduction, which indicates an ill conditioned matrix.

  See Also:
    - :func:`jax.numpy.poly`: Finds the polynomial coefficients of the given
      sequence of roots.
    - :func:`jax.numpy.polyval`: Evaluate a polynomial at specific values.
    - :func:`jax.numpy.roots`: Computes the roots of a polynomial for given
      coefficients.

  Examples:
    >>> x = jnp.array([3., 6., 9., 4.])
    >>> y = jnp.array([[0, 1, 2],
    ...                [2, 5, 7],
    ...                [8, 4, 9],
    ...                [1, 6, 3]])
    >>> p = jnp.polyfit(x, y, 2)
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(p)
    [[ 0.2  -0.35 -0.14]
     [-1.17  4.47  2.96]
     [ 1.95 -8.21 -5.93]]

    If ``full=True``, returns a tuple of arrays as follows:

    >>> p, resids, rank, s, rcond = jnp.polyfit(x, y, 2, full=True)
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print("Polynomial Coefficients:", "\n", p, "\n",
    ...         "Residuals:", resids, "\n",
    ...         "Rank:", rank, "\n",
    ...         "s:", s, "\n",
    ...         "rcond:", rcond)
    Polynomial Coefficients:
    [[ 0.2  -0.35 -0.14]
    [-1.17  4.47  2.96]
    [ 1.95 -8.21 -5.93]]
    Residuals: [0.37 5.94 0.61]
    Rank: 3
    s: [1.67 0.47 0.04]
    rcond: 4.7683716e-07

    If ``cov=True`` and ``full=False``, returns a tuple of arrays having
    polynomial coefficients and covariance matrix.

    >>> p, C = jnp.polyfit(x, y, 2, cov=True)
    >>> p.shape, C.shape
    ((3, 3), (3, 3, 3))
  """
  if w is None:
    x_arr, y_arr = ensure_arraylike("polyfit", x, y)
  else:
    x_arr, y_arr, w = ensure_arraylike("polyfit", x, y, w)
  del x, y
  deg = core.concrete_or_error(int, deg, "deg must be int")
  order = deg + 1
  if deg < 0:
    raise ValueError("expected deg >= 0")
  if x_arr.ndim != 1:
    raise TypeError("expected 1D vector for x")
  if x_arr.size == 0:
    raise TypeError("expected non-empty vector for x")
  if y_arr.ndim < 1 or y_arr.ndim > 2:
    raise TypeError("expected 1D or 2D array for y")
  if x_arr.shape[0] != y_arr.shape[0]:
    raise TypeError("expected x and y to have same length")

  if rcond is None:
    rcond = len(x_arr) * float(finfo(x_arr.dtype).eps)
  rcond = core.concrete_or_error(float, rcond, "rcond must be float")
  # set up least squares equation for powers of x
  lhs = vander(x_arr, order)
  rhs = y_arr

  # apply weighting
  if w is not None:
    w_arr, = promote_dtypes_inexact(w)
    if w_arr.ndim != 1:
      raise TypeError("expected a 1-d array for weights")
    if w_arr.shape[0] != y_arr.shape[0]:
      raise TypeError("expected w and y to have the same length")
    lhs *= w_arr[:, np.newaxis]
    if rhs.ndim == 2:
      rhs *= w_arr[:, np.newaxis]
    else:
      rhs *= w_arr

  # scale lhs to improve condition number and solve
  scale = sqrt((lhs*lhs).sum(axis=0))
  lhs /= scale[np.newaxis, :]
  c, resids, rank, s = linalg.lstsq(lhs, rhs, rcond)

  # Broadcasting scale coefficients
  if c.ndim > 1:
    # For multi-dimensional output, make scale (1, order) to divide
    # across the c.T of shape (num_rhs, order)
    c = (c.T / scale[np.newaxis, :]).T
  else:
    # Simple case for 1D output
    c = c / scale

  if full:
    assert rcond is not None
    return c, resids, rank, s, lax.asarray(rcond)
  elif cov:
    Vbase = linalg.inv(dot(lhs.T, lhs))
    Vbase /= outer(scale, scale)

    if cov == "unscaled":
      fac = array(1.0)
    else:
      if len(x_arr) <= order:
        raise ValueError("the number of data points must exceed order"
                         " to scale the covariance matrix")
      fac = resids / (len(x_arr) - order)

    if y_arr.ndim == 1:
      fac = atleast_1d(fac)[np.newaxis]
      # For 1D output, simple scalar multiplication
      return c, Vbase * fac
    else:
      # For multiple rhs, broadcast fac to match shape
      return c, Vbase[:, :, np.newaxis] * atleast_1d(fac)[np.newaxis, np.newaxis, :]
  else:
    return c

