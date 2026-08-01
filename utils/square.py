
def square(a: TensorLikeType) -> TensorLikeType:
    return mul(a, a)


def square(g: jit_utils.GraphContext, self):
    return g.op("Mul", self, self)


def square(x):
    return x**2


def square(t, duty=0.5):
    """
    Return a periodic square-wave waveform.

    The square wave has a period ``2*pi``, has value +1 from 0 to
    ``2*pi*duty`` and -1 from ``2*pi*duty`` to ``2*pi``. `duty` must be in
    the interval ``[0,1]``.

    Note that this is not band-limited.  It produces an infinite number
    of harmonics, which are aliased back and forth across the frequency
    spectrum.

    Parameters
    ----------
    t : array_like
        The input time array.
    duty : array_like, optional
        Duty cycle.  Default is 0.5 (50% duty cycle).
        If an array, causes wave shape to change over time, and must be the
        same length as t.

    Returns
    -------
    y : ndarray
        Output array containing the square waveform.

    Examples
    --------
    A 5 Hz waveform sampled at 500 Hz for 1 second:

    >>> import numpy as np
    >>> from scipy import signal
    >>> import matplotlib.pyplot as plt
    >>> t = np.linspace(0, 1, 500, endpoint=False)
    >>> plt.plot(t, signal.square(2 * np.pi * 5 * t))
    >>> plt.ylim(-2, 2)

    A pulse-width modulated sine wave:

    >>> plt.figure()
    >>> sig = np.sin(2 * np.pi * t)
    >>> pwm = signal.square(2 * np.pi * 30 * t, duty=(sig + 1)/2)
    >>> plt.subplot(2, 1, 1)
    >>> plt.plot(t, sig)
    >>> plt.subplot(2, 1, 2)
    >>> plt.plot(t, pwm)
    >>> plt.ylim(-1.5, 1.5)

    """
    xp = array_namespace(t, duty)
    t, w = xp_promote(t, duty, xp=xp, force_floating=True, broadcast=True)

    y = xp.zeros_like(t)

    # width must be between 0 and 1 inclusive
    mask1 = (w > 1) | (w < 0)
    y = xpx.at(y, mask1).set(xp.nan)

    # on the interval 0 to duty*2*pi function is 1
    tmod = t % (2 * xp.pi)
    mask2 = ~mask1 & (tmod < w*2*xp.pi)
    y = xpx.at(y, mask2).set(1)

    # on the interval duty*2*pi to 2*pi function is -1
    mask3 = ~(mask1 | mask2)
    y = xpx.at(y, mask3).set(-1)
    return y


def square(operand: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return SquareOp(operand=operand, results=results, loc=loc, ip=ip).result


def square(x: ArrayLike) -> Array:
  r"""Elementwise square: :math:`x^2`."""
  return square_p.bind(x)


def square(x: ArrayLike, /) -> Array:
  """Calculate element-wise square of the input array.

  JAX implementation of :obj:`numpy.square`.

  Args:
    x: input array or scalar.

  Returns:
    An array containing the square of the elements of ``x``.

  Note:
    ``jnp.square`` is equivalent to computing ``jnp.power(x, 2)``.

  See also:
    - :func:`jax.numpy.sqrt`: Calculates the element-wise non-negative square root
      of the input array.
    - :func:`jax.numpy.power`: Calculates the element-wise base ``x1`` exponential
      of ``x2``.
    - :func:`jax.lax.integer_pow`: Computes element-wise power :math:`x^y`, where
      :math:`y` is a fixed integer.
    - :func:`jax.numpy.float_power`: Computes the first array raised to the power
      of second array, element-wise, by promoting to the inexact dtype.

  Examples:
    >>> x = jnp.array([3, -2, 5.3, 1])
    >>> jnp.square(x)
    Array([ 9.      ,  4.      , 28.090002,  1.      ], dtype=float32)
    >>> jnp.power(x, 2)
    Array([ 9.      ,  4.      , 28.090002,  1.      ], dtype=float32)

    For integer inputs:

    >>> x1 = jnp.array([2, 4, 5, 6])
    >>> jnp.square(x1)
    Array([ 4, 16, 25, 36], dtype=int32)

    For complex-valued inputs:

    >>> x2 = jnp.array([1-3j, -1j, 2])
    >>> jnp.square(x2)
    Array([-8.-6.j, -1.+0.j,  4.+0.j], dtype=complex64)
  """
  x = ensure_arraylike("square", x)
  x, = promote_dtypes_numeric(x)
  return lax.square(x)

