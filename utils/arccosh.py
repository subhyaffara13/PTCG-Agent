
def arccosh(x: ArrayLike, /) -> Array:
  r"""Calculate element-wise inverse of hyperbolic cosine of input.

  JAX implementation of :obj:`numpy.arccosh`.

  The inverse of hyperbolic cosine is defined by:

  .. math::

    arccosh(x) = \ln(x + \sqrt{x^2 - 1})

  Args:
    x: input array or scalar.

  Returns:
    An array of same shape as ``x`` containing the inverse of hyperbolic cosine
    of each element of ``x``, promoting to inexact dtype.

  Note:
    - ``jnp.arccosh`` returns ``nan`` for real-values in the range ``[-inf, 1)``.
    - ``jnp.arccosh`` follows the branch cut convention of :obj:`numpy.arccosh`
      for complex inputs.

  See also:
    - :func:`jax.numpy.cosh`: Computes the element-wise hyperbolic cosine of the
      input.
    - :func:`jax.numpy.arcsinh`: Computes the element-wise inverse of hyperbolic
      sine of the input.
    - :func:`jax.numpy.arctanh`: Computes the element-wise inverse of hyperbolic
      tangent of the input.

  Examples:
    >>> x = jnp.array([[1, 3, -4],
    ...                [-5, 2, 7]])
    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   jnp.arccosh(x)
    Array([[0.   , 1.763,   nan],
           [  nan, 1.317, 2.634]], dtype=float32)

    For complex-valued input:

    >>> x1 = jnp.array([-jnp.inf+0j, 1+2j, -5+0j])
    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   jnp.arccosh(x1)
    Array([  inf+3.142j, 1.529+1.144j, 2.292+3.142j], dtype=complex64)
  """
  # Note: arccosh is multi-valued for complex input, and lax.acosh
  # uses a different convention than np.arccosh.
  result = lax.acosh(*promote_args_inexact("arccosh", x))
  jnp_error._set_error_if_nan(result)
  if dtypes.issubdtype(result.dtype, np.complexfloating):
    result = _where(real(result) < 0, lax.neg(result), result)
  return result

