
def sici(x: ArrayLike) -> tuple[Array, Array]:
  r"""Sine and cosine integrals.

  JAX implementation of :obj:`scipy.special.sici`.

  .. math::

    \mathrm{Si}(x) = \int_0^x \frac{\sin t}{t} \, dt

  .. math::

    \mathrm{Ci}(x) = \gamma + \ln(x) + \int_0^x \frac{\cos t - 1}{t} \, dt

  where :math:`\gamma` is the Euler–Mascheroni constant.

  Args:
    x: array-like, real-valued input.

  Returns:
    A tuple of two arrays, each with the same shape as `x`:
      - The first array contains the sine integral values `Si(x)`.
      - The second array contains the cosine integral values `Ci(x)`.

  See also:
    - :func:`jax.numpy.sinc`
  """

  x, = promote_args_inexact("sici", x)

  if dtypes.issubdtype(x.dtype, np.complexfloating):
    raise ValueError(
      f"Argument `x` to sici must be real-valued. Got dtype {x.dtype}."
    )

  x_abs = jnp.abs(x)

  si_series, ci_series = _sici_series(x_abs)
  si_asymp,  ci_asymp  = _sici_asympt(x_abs)
  si_approx, ci_approx  = _sici_approx(x_abs)

  cond1 = x_abs <= 4
  cond2 = (x_abs > 4) & (x_abs <= 1e9)

  si = jnp.select([cond1, cond2], [si_series, si_asymp], si_approx)
  ci = jnp.select([cond1, cond2], [ci_series, ci_asymp], ci_approx)

  si = jnp.sign(x) * si
  ci = jnp.where(isneginf(x), np.nan, ci)

  return si, ci

