
def conjugate(x: ArrayLike, /) -> Array:
  """Return element-wise complex-conjugate of the input.

  JAX implementation of :obj:`numpy.conjugate`.

  Args:
    x: inpuat array or scalar.

  Returns:
    An array containing the complex-conjugate of ``x``.

  See also:
    - :func:`jax.numpy.real`: Returns the element-wise real part of the complex
      argument.
    - :func:`jax.numpy.imag`: Returns the element-wise imaginary part of the
      complex argument.

  Examples:
    >>> jnp.conjugate(3)
    Array(3, dtype=int32, weak_type=True)
    >>> x = jnp.array([2-1j, 3+5j, 7])
    >>> jnp.conjugate(x)
    Array([2.+1.j, 3.-5.j, 7.-0.j], dtype=complex64)
  """
  x = ensure_arraylike("conjugate", x)
  return lax.conj(x) if np.iscomplexobj(x) else lax.asarray(x)

