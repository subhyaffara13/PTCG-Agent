
def arcsinh(x: ArrayLike, /) -> Array:
  r"""Calculate element-wise inverse of hyperbolic sine of input.

  JAX implementation of :obj:`numpy.arcsinh`.

  The inverse of hyperbolic sine is defined by:

  .. math::

    arcsinh(x) = \ln(x + \sqrt{1 + x^2})

  Args:
    x: input array or scalar.

  Returns:
    An array of same shape as ``x`` containing the inverse of hyperbolic sine of
    each element of ``x``, promoting to inexact dtype.

  Note:
    - ``jnp.arcsinh`` returns ``nan`` for values outside the range ``(-inf, inf)``.
    - ``jnp.arcsinh`` follows the branch cut convention of :obj:`numpy.arcsinh`
      for complex inputs.

  See also:
    - :func:`jax.numpy.sinh`: Computes the element-wise hyperbolic sine of the input.
    - :func:`jax.numpy.arccosh`: Computes the element-wise inverse of hyperbolic
      cosine of the input.
    - :func:`jax.numpy.arctanh`: Computes the element-wise inverse of hyperbolic
      tangent of the input.

  Examples:
    >>> x = jnp.array([[-2, 3, 1],
    ...                [4, 9, -5]])
    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   jnp.arcsinh(x)
    Array([[-1.444,  1.818,  0.881],
           [ 2.095,  2.893, -2.312]], dtype=float32)

    For complex-valued inputs:

    >>> x1 = jnp.array([4-3j, 2j])
    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   jnp.arcsinh(x1)
    Array([2.306-0.634j, 1.317+1.571j], dtype=complex64)
  """
  return lax.asinh(*promote_args_inexact('arcsinh', x))

