
def generate_knots(x, y, *, w=None, xb=None, xe=None,
                   k=3, s=0, nest=None, bc_type=None):
    """Generate knot vectors until the Least SQuares (LSQ) criterion is satified.

    Parameters
    ----------
    x, y : array_like
        The data points defining the curve ``y = f(x)``.
    w : array_like, optional
        Weights.
    xb : float, optional
        The boundary of the approximation interval. If None (default),
        is set to ``x[0]``.
    xe : float, optional
        The boundary of the approximation interval. If None (default),
        is set to ``x[-1]``.
    k : int, optional
        The spline degree. Default is cubic, ``k = 3``.
    s : float, optional
        The smoothing factor. Default is ``s = 0``.
    nest : int, optional
        Stop when at least this many knots are placed.
          ends are equivalent.
    bc_type : str, optional
        Boundary conditions.
        Default is `"not-a-knot"`.
        The following boundary conditions are recognized:

        * ``"not-a-knot"`` (default): The first and second segments are the
          same polynomial. This is equivalent to having ``bc_type=None``.
        * ``"periodic"``: The values and the first ``k-1`` derivatives at the
          ends are equivalent.

    Yields
    ------
    t : ndarray
        Knot vectors with an increasing number of knots.
        The generator is finite: it stops when the smoothing critetion is
        satisfied, or when then number of knots exceeds the maximum value:
        the user-provided `nest` or `x.size + k + 1` --- which is the knot vector
        for the interpolating spline.

    Examples
    --------
    Generate some noisy data and fit a sequence of LSQ splines:

    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> from scipy.interpolate import make_lsq_spline, generate_knots
    >>> rng = np.random.default_rng(12345)
    >>> x = np.linspace(-3, 3, 50)
    >>> y = np.exp(-x**2) + 0.1 * rng.standard_normal(size=50)

    >>> knots = list(generate_knots(x, y, s=1e-10))
    >>> for t in knots[::3]:
    ...     spl = make_lsq_spline(x, y, t)
    ...     xs = xs = np.linspace(-3, 3, 201)
    ...     plt.plot(xs, spl(xs), '-', label=f'n = {len(t)}', lw=3, alpha=0.7)
    >>> plt.plot(x, y, 'o', label='data')
    >>> plt.plot(xs, np.exp(-xs**2), '--')
    >>> plt.legend()

    Note that increasing the number of knots make the result follow the data
    more and more closely.

    Also note that a step of the generator may add multiple knots:

    >>> [len(t) for t in knots]
    [8, 9, 10, 12, 16, 24, 40, 48, 52, 54]

    Notes
    -----
    The routine generates successive knots vectors of increasing length, starting
    from ``2*(k+1)`` to ``len(x) + k + 1``, trying to make knots more dense
    in the regions where the deviation of the LSQ spline from data is large.

    When the maximum number of knots, ``len(x) + k + 1`` is reached
    (this happens when ``s`` is small and ``nest`` is large), the generator
    stops, and the last output is the knots for the interpolation with the
    not-a-knot boundary condition.

    Knots are located at data sites, unless ``k`` is even and the number of knots
    is ``len(x) + k + 1``. In that case, the last output of the generator
    has internal knots at Greville sites, ``(x[1:] + x[:-1]) / 2``.

    .. versionadded:: 1.15.0

    """
    xp = array_namespace(x, y, w)
    bc_type = _validate_bc_type(bc_type)
    periodic = bc_type == 'periodic'

    if s == 0:
        if nest is not None or w is not None:
            raise ValueError("s == 0 is interpolation only")
        # For special-case k=1 (e.g., Lyche and Morken, Eq.(2.16)),
        # _not_a_knot produces desired knot vector
        if periodic and k > 1:
            t = _periodic_knots(x, k)
        else:
            t = _not_a_knot(x, k)
        yield xp.asarray(t)
        return

    x, y, w, k, s, xb, xe = _validate_inputs(
        x, y, w, k, s, xb, xe, parametric=np.ndim(y) == 2,
        periodic=periodic
    )

    yield from _generate_knots_impl(x, y, w, xb, xe, k, s, nest, periodic, xp=xp)

