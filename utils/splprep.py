
def splprep(x, w=None, u=None, ub=None, ue=None, k=3, task=0, s=None, t=None,
            full_output=0, nest=None, per=0, quiet=1):
    # see the docstring of `_fitpack_py/splprep`
    if task <= 0:
        _parcur_cache = {'t': array([], float), 'wrk': array([], float),
                         'iwrk': array([], np.int32), 'u': array([], float),
                         'ub': 0, 'ue': 1}
    x = atleast_1d(x)
    idim, m = x.shape
    if per:
        for i in range(idim):
            if x[i][0] != x[i][-1]:
                if not quiet:
                    warnings.warn(
                        RuntimeWarning(f'Setting x[{i}][{m}]=x[{i}][0]'),
                        stacklevel=2
                    )
                x[i][-1] = x[i][0]
    if not 0 < idim < 11:
        raise TypeError('0 < idim < 11 must hold')
    if w is None:
        w = ones(m, float)
    else:
        w = atleast_1d(w)
    ipar = (u is not None)
    if ipar:
        _parcur_cache['u'] = u
        if ub is None:
            _parcur_cache['ub'] = u[0]
        else:
            _parcur_cache['ub'] = ub
        if ue is None:
            _parcur_cache['ue'] = u[-1]
        else:
            _parcur_cache['ue'] = ue
    else:
        _parcur_cache['u'] = zeros(m, float)
    if not (1 <= k <= 5):
        raise TypeError(f'1 <= k= {k} <=5 must hold')
    if not (-1 <= task <= 1):
        raise TypeError('task must be -1, 0 or 1')
    if (not len(w) == m) or (ipar == 1 and (not len(u) == m)):
        raise TypeError('Mismatch of input dimensions')
    if s is None:
        s = m - sqrt(2*m)
    if t is None and task == -1:
        raise TypeError('Knots must be given for task=-1')
    if t is not None:
        _parcur_cache['t'] = atleast_1d(t)
    n = len(_parcur_cache['t'])
    if task == -1 and n < 2*k + 2:
        raise TypeError('There must be at least 2*k+2 knots for task=-1')
    if m <= k:
        raise TypeError('m > k must hold')
    if nest is None:
        nest = m + 2*k

    if (task >= 0 and s == 0) or (nest < 0):
        if per:
            nest = m + 2*k
        else:
            nest = m + k + 1
    nest = max(nest, 2*k + 3)
    u = _parcur_cache['u']
    ub = _parcur_cache['ub']
    ue = _parcur_cache['ue']
    t = _parcur_cache['t']
    wrk = _parcur_cache['wrk']
    iwrk = _parcur_cache['iwrk']
    t, c, o = _fitpack.parcur(ravel(x, 'F'), w, u, ub, ue, k, task, ipar, s,
                              t, nest, wrk, iwrk, per)
    _parcur_cache['u'] = o['u']
    _parcur_cache['ub'] = o['ub']
    _parcur_cache['ue'] = o['ue']
    _parcur_cache['t'] = t
    _parcur_cache['wrk'] = o['wrk']
    _parcur_cache['iwrk'] = o['iwrk']
    ier = o['ier']
    fp = o['fp']
    n = len(t)
    u = o['u']
    c = c.reshape((idim, n - k - 1))
    tcku = [t, list(c), k], u
    if ier <= 0 and not quiet:
        warnings.warn(
            RuntimeWarning(
                _iermess[ier][0] + f"\tk={k} n={len(t)} m={m} fp={fp} s={s}"
            ),
            stacklevel=2
        )
    if ier > 0 and not full_output:
        if ier in [1, 2, 3]:
            warnings.warn(RuntimeWarning(_iermess[ier][0]), stacklevel=2)
        else:
            try:
                raise _iermess[ier][1](_iermess[ier][0])
            except KeyError as e:
                raise _iermess['unknown'][1](_iermess['unknown'][0]) from e
    if full_output:
        try:
            return tcku, fp, ier, _iermess[ier][0]
        except KeyError:
            return tcku, fp, ier, _iermess['unknown'][0]
    else:
        return tcku


def splprep(x, w=None, u=None, ub=None, ue=None, k=3, task=0, s=None, t=None,
            full_output=0, nest=None, per=0, quiet=1):
    """
    Find the B-spline representation of an N-D curve.

    .. legacy:: function

        Specifically, we recommend using `make_splprep` in new code.

    Given a list of N rank-1 arrays, `x`, which represent a curve in
    N-dimensional space parametrized by `u`, find a smooth approximating
    spline curve g(`u`). Uses the FORTRAN routine parcur from FITPACK.

    Parameters
    ----------
    x : array_like
        A list of sample vector arrays representing the curve.
    w : array_like, optional
        Strictly positive rank-1 array of weights the same length as `x[0]`.
        The weights are used in computing the weighted least-squares spline
        fit. If the errors in the `x` values have standard-deviation given by
        the vector d, then `w` should be 1/d. Default is ``ones(len(x[0]))``.
    u : array_like, optional
        An array of parameter values. If not given, these values are
        calculated automatically as ``M = len(x[0])``, where

        - ``v[0] = 0``
        - ``v[i] = v[i-1] + distance(`x[i]`, `x[i-1]`)``
        - ``u[i] = v[i] / v[M-1]``

    ub, ue : int, optional
        The end-points of the parameters interval.  Defaults to
        u[0] and u[-1].
    k : int, optional
        Degree of the spline. Cubic splines are recommended.
        Even values of `k` should be avoided especially with a small s-value.
        ``1 <= k <= 5``, default is 3.
    task : int, optional
        If task==0 (default), find t and c for a given smoothing factor, s.
        If task==1, find t and c for another value of the smoothing factor, s.
        There must have been a previous call with task=0 or task=1
        for the same set of data.
        If task=-1 find the weighted least square spline for a given set of
        knots, t.
    s : float, optional
        A smoothing condition.  The amount of smoothness is determined by
        satisfying the conditions: ``sum((w * (y - g))**2,axis=0) <= s``,
        where g(x) is the smoothed interpolation of (x,y).  The user can
        use `s` to control the trade-off between closeness and smoothness
        of fit.  Larger `s` means more smoothing while smaller values of `s`
        indicate less smoothing. Recommended values of `s` depend on the
        weights, w.  If the weights represent the inverse of the
        standard-deviation of y, then a good `s` value should be found in
        the range ``(m-sqrt(2*m),m+sqrt(2*m))``, where m is the number of
        data points in x, y, and w.
    t : array, optional
        The knots needed for ``task=-1``.
        There must be at least ``2*k+2`` knots.
    full_output : int, optional
        If non-zero, then return optional outputs.
    nest : int, optional
        An over-estimate of the total number of knots of the spline to
        help in determining the storage space.  By default nest=m/2.
        Always large enough is nest=m+k+1.
    per : int, optional
       If non-zero, data points are considered periodic with period
       ``x[m-1] - x[0]`` and a smooth periodic spline approximation is
       returned.  Values of ``y[m-1]`` and ``w[m-1]`` are not used.
    quiet : int, optional
         Non-zero to suppress messages.

    Returns
    -------
    tck : tuple
        A tuple, ``(t,c,k)`` containing the vector of knots, the B-spline
        coefficients, and the degree of the spline.
    u : array
        An array of the values of the parameter.
    fp : float
        The weighted sum of squared residuals of the spline approximation.
    ier : int
        An integer flag about splrep success.  Success is indicated
        if ier<=0. If ier in [1,2,3] an error occurred but was not raised.
        Otherwise an error is raised.
    msg : str
        A message corresponding to the integer flag, ier.

    See Also
    --------
    splrep, splev, sproot, spalde, splint,
    bisplrep, bisplev
    UnivariateSpline, BivariateSpline
    BSpline
    make_interp_spline

    Notes
    -----
    See `splev` for evaluation of the spline and its derivatives.
    The number of dimensions N must be smaller than 11.

    The number of coefficients in the `c` array is ``k+1`` less than the number
    of knots, ``len(t)``. This is in contrast with `splrep`, which zero-pads
    the array of coefficients to have the same length as the array of knots.
    These additional coefficients are ignored by evaluation routines, `splev`
    and `BSpline`.

    References
    ----------
    .. [1] P. Dierckx, "Algorithms for smoothing data with periodic and
        parametric splines, Computer Graphics and Image Processing",
        20 (1982) 171-184.
    .. [2] P. Dierckx, "Algorithms for smoothing data with periodic and
        parametric splines", report tw55, Dept. Computer Science,
        K.U.Leuven, 1981.
    .. [3] P. Dierckx, "Curve and surface fitting with splines", Monographs on
        Numerical Analysis, Oxford University Press, 1993.

    Examples
    --------
    Generate a discretization of a limacon curve in the polar coordinates:

    >>> import numpy as np
    >>> phi = np.linspace(0, 2.*np.pi, 40)
    >>> r = 0.5 + np.cos(phi)         # polar coords
    >>> x, y = r * np.cos(phi), r * np.sin(phi)    # convert to cartesian

    And interpolate:

    >>> from scipy.interpolate import splprep, splev
    >>> tck, u = splprep([x, y], s=0)
    >>> new_points = splev(u, tck)

    Notice that (i) we force interpolation by using ``s=0``,
    (ii) the parameterization, ``u``, is generated automatically.
    Now plot the result:

    >>> import matplotlib.pyplot as plt
    >>> fig, ax = plt.subplots()
    >>> ax.plot(x, y, 'ro')
    >>> ax.plot(new_points[0], new_points[1], 'r-')
    >>> plt.show()

    """

    res = _impl.splprep(x, w, u, ub, ue, k, task, s, t, full_output, nest, per,
                        quiet)
    return res

