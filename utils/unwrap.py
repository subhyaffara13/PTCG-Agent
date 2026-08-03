import re

def unwrap(s):
    r"""
    Given a multi-line string, return an unwrapped version.

    >>> wrapped = wrap(lorem_ipsum)
    >>> wrapped.count('\n')
    20
    >>> unwrapped = unwrap(wrapped)
    >>> unwrapped.count('\n')
    1
    >>> print(unwrapped)
    Lorem ipsum dolor sit amet, consectetur adipiscing ...
    Curabitur pretium tincidunt lacus. Nulla gravida orci ...

    """
    paragraphs = re.split(r'\n\n+', s)
    cleaned = (para.replace('\n', ' ') for para in paragraphs)
    return '\n'.join(cleaned)


def unwrap(p, discont=None, axis=-1, *, period=2 * pi):
    r"""
    Unwrap by taking the complement of large deltas with respect to the period.

    This unwraps a signal `p` by changing elements which have an absolute
    difference from their predecessor of more than ``max(discont, period/2)``
    to their `period`-complementary values.

    For the default case where `period` is :math:`2\pi` and `discont` is
    :math:`\pi`, this unwraps a radian phase `p` such that adjacent differences
    are never greater than :math:`\pi` by adding :math:`2k\pi` for some
    integer :math:`k`.

    Parameters
    ----------
    p : array_like
        Input array.
    discont : float, optional
        Maximum discontinuity between values, default is ``period/2``.
        Values below ``period/2`` are treated as if they were ``period/2``.
        To have an effect different from the default, `discont` should be
        larger than ``period/2``.
    axis : int, optional
        Axis along which unwrap will operate, default is the last axis.
    period : float, optional
        Size of the range over which the input wraps. By default, it is
        ``2 pi``.

        .. versionadded:: 1.21.0

    Returns
    -------
    out : ndarray
        Output array.

    See Also
    --------
    rad2deg, deg2rad

    Notes
    -----
    If the discontinuity in `p` is smaller than ``period/2``,
    but larger than `discont`, no unwrapping is done because taking
    the complement would only make the discontinuity larger.

    Examples
    --------
    >>> import numpy as np

    >>> phase = np.linspace(0, np.pi, num=5)
    >>> phase[3:] += np.pi
    >>> phase
    array([ 0.        ,  0.78539816,  1.57079633,  5.49778714,  6.28318531]) # may vary
    >>> np.unwrap(phase)
    array([ 0.        ,  0.78539816,  1.57079633, -0.78539816,  0.        ]) # may vary
    >>> np.unwrap([0, 1, 2, -1, 0], period=4)
    array([0, 1, 2, 3, 4])
    >>> np.unwrap([ 1, 2, 3, 4, 5, 6, 1, 2, 3], period=6)
    array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    >>> np.unwrap([2, 3, 4, 5, 2, 3, 4, 5], period=4)
    array([2, 3, 4, 5, 6, 7, 8, 9])
    >>> phase_deg = np.mod(np.linspace(0 ,720, 19), 360) - 180
    >>> np.unwrap(phase_deg, period=360)
    array([-180., -140., -100.,  -60.,  -20.,   20.,   60.,  100.,  140.,
            180.,  220.,  260.,  300.,  340.,  380.,  420.,  460.,  500.,
            540.])

    This example plots the unwrapping of the wrapped input signal `w`.
    First generate `w`, then apply `unwrap` to get `u`.

    >>> t = np.linspace(0, 25, 801)
    >>> w = np.mod(1.5 * np.sin(1.1 * t + 0.26) * (1 - t / 6 + (t / 23) ** 3), 2.0) - 1
    >>> u = np.unwrap(w, period=2.0)

    Plot `w` and `u`.

    >>> import matplotlib.pyplot as plt
    >>> plt.plot(t, w, label='w (a signal wrapped to [-1, 1])')
    >>> plt.plot(t, u, linewidth=2.5, alpha=0.5, label='unwrap(w, period=2)')
    >>> plt.xlabel('t')
    >>> plt.grid(alpha=0.6)
    >>> plt.legend(framealpha=1, shadow=True)
    >>> plt.show()
    """
    p = asarray(p)
    nd = p.ndim
    dd = diff(p, axis=axis)
    if discont is None:
        discont = period / 2
    slice1 = [slice(None, None)] * nd     # full slices
    slice1[axis] = slice(1, None)
    slice1 = tuple(slice1)
    dtype = np.result_type(dd, period)
    if _nx.issubdtype(dtype, _nx.integer):
        interval_high, rem = divmod(period, 2)
        boundary_ambiguous = rem == 0
    else:
        interval_high = period / 2
        boundary_ambiguous = True
    interval_low = -interval_high
    ddmod = mod(dd - interval_low, period) + interval_low
    if boundary_ambiguous:
        # for `mask = (abs(dd) == period/2)`, the above line made
        # `ddmod[mask] == -period/2`. correct these such that
        # `ddmod[mask] == sign(dd[mask])*period/2`.
        _nx.copyto(ddmod, interval_high,
                   where=(ddmod == interval_low) & (dd > 0))
    ph_correct = ddmod - dd
    _nx.copyto(ph_correct, 0, where=abs(dd) < discont)
    up = array(p, copy=True, dtype=dtype)
    up[slice1] = p[slice1] + ph_correct.cumsum(axis)
    return up


def unwrap(p: ArrayLike, discont: ArrayLike | None = None,
           axis: int = -1, period: ArrayLike = 2 * np.pi) -> Array:
  """Unwrap a periodic signal.

  JAX implementation of :func:`numpy.unwrap`.

  Args:
    p: input array
    discont: the maximum allowable discontinuity in the sequence. The
      default is ``period / 2``
    axis: the axis along which to unwrap; defaults to -1
    period: the period of the signal, which defaults to :math:`2\\pi`

  Returns:
    An unwrapped copy of ``p``.

  Notes:
    This implementation follows that of :func:`numpy.unwrap`, and is not
    well-suited for integer-period unwrapping of narrow-width integers
    (e.g. `int8`, `int16`) or unsigned integers.

  Examples:
    Consider a situation in which you are making measurements of the position of
    a rotating disk via the ``x`` and ``y`` locations of some point on that disk.
    The underlying variable is an always-increasing angle which we'll generate
    this way, using degrees for ease of representation:

    >>> rng = np.random.default_rng(0)
    >>> theta = rng.integers(0, 90, size=(20,)).cumsum()
    >>> theta
    array([ 76, 133, 179, 203, 230, 233, 239, 240, 255, 328, 386, 468, 513,
           567, 654, 719, 775, 823, 873, 957])

    Our observations of this angle are the ``x`` and ``y`` coordinates, given by
    the sine and cosine of this underlying angle:

    >>> x, y = jnp.sin(jnp.deg2rad(theta)), jnp.cos(jnp.deg2rad(theta))

    Now, say that given these ``x`` and ``y`` coordinates, we wish to recover
    the original angle ``theta``. We might do this via the :func:`atan2` function:

    >>> theta_out = jnp.rad2deg(jnp.atan2(x, y)).round()
    >>> theta_out
    Array([  76.,  133.,  179., -157., -130., -127., -121., -120., -105.,
            -32.,   26.,  108.,  153., -153.,  -66.,   -1.,   55.,  103.,
            153., -123.], dtype=float32)

    The first few values match the input angle ``theta`` above, but after this the
    values are wrapped because the ``sin`` and ``cos`` observations obscure the phase
    information. The purpose of the :func:`unwrap` function is to recover the original
    signal from this wrapped view of it:

    >>> jnp.unwrap(theta_out, period=360)
    Array([ 76., 133., 179., 203., 230., 233., 239., 240., 255., 328., 386.,
           468., 513., 567., 654., 719., 775., 823., 873., 957.],      dtype=float32)

    It does this by assuming that the true underlying sequence does not differ by more than
    ``discont`` (which defaults to ``period / 2``) within a single step, and when it encounters
    a larger discontinuity it adds factors of the period to the data. For periodic signals
    that satisfy this assumption, :func:`unwrap` can recover the original phased signal.
  """
  p = util.ensure_arraylike("unwrap", p)
  p, period = util.promote_dtypes(p, period)

  if issubdtype(p.dtype, np.complexfloating):
    raise ValueError("jnp.unwrap does not support complex inputs.")
  if p.shape[axis] == 0:
    return p

  if discont is None:
    discont = period / 2
  if dtypes.issubdtype(p.dtype, np.integer):
    interval = period // 2
  else:
    interval = period / 2

  dd = diff(p, axis=axis)
  ddmod = ufuncs.mod(dd + interval, period) - interval
  ddmod = where((ddmod == -interval) & (dd > 0), interval, ddmod)

  ph_correct = where(ufuncs.abs(dd) < discont, 0, ddmod - dd)

  up = concatenate((
    lax_slicing.slice_in_dim(p, 0, 1, axis=axis),
    lax_slicing.slice_in_dim(p, 1, None, axis=axis) + reductions.cumsum(ph_correct, axis=axis)
  ), axis=axis)

  return up


def unwrap(url):
    """unwrap('<URL:type://host/path>') --> 'type://host/path'."""
    url = str(url).strip()
    if url[:1] == '<' and url[-1:] == '>':
        url = url[1:-1].strip()
    if url[:4] == 'URL:': url = url[4:].strip()
    return url

