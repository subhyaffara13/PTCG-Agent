
def owens_t(h: ArrayLike, a: ArrayLike) -> Array:
  r"""Owen's T function.

  JAX implementation of :obj:`scipy.special.owens_t`.

  Computes Owen's T function:

  .. math::

     T(h, a) = \frac{1}{2\pi} \int_0^a
         \frac{\exp\!\left(-\tfrac{1}{2}h^2(1+x^2)\right)}{1+x^2} \, dx

  Computed via 13-point Gauss-type quadrature on the canonical integral
  form (Patefield & Tandy 2000 method T5).
  The full 18-region dispatch from Patefield & Tandy is
  intentionally avoided because XLA evaluates every branch of a
  ``where`` / ``select`` unconditionally, which turns per-region
  dispatch into added cost rather than savings.

  Args:
    h: array_like, real-valued.
    a: array_like, real-valued.

  Returns:
    Array of Owen's T values with dtype matching the promoted inputs.

  See also:
    :func:`jax.scipy.special.ndtr`
  """
  h, a = promote_args_inexact("owens_t", h, a)
  return _owens_t_impl(h, a)

