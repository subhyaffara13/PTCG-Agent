
def bitwise_not(a):
    return prims.bitwise_not(a)


def bitwise_not(g: jit_utils.GraphContext, input):
    if not symbolic_helper._is_bool(input):
        raise errors.SymbolicValueError(
            "ONNX export does NOT support exporting bitwise Not "
            "for non-boolean input values",
            input,
        )
    return g.op("Not", input)


def bitwise_not(x: ArrayLike) -> Array:
  r"""Elementwise NOT: :math:`\neg x`.

  This function lowers directly to the `stablehlo.not`_ operation.

  Args:
    x: Input array. Must have boolean or integer dtype.

  Returns:
    An array of the same shape and dtype as ``x`` containing the bitwise
    inversion of each entry.

  See also:
    - :func:`jax.numpy.invert`: NumPy wrapper for this API, also accessible
      via the ``~x`` operator on JAX arrays.
    - :func:`jax.lax.bitwise_and`: Elementwise AND.
    - :func:`jax.lax.bitwise_or`: Elementwise OR.
    - :func:`jax.lax.bitwise_xor`: Elementwise exclusive OR.

  .. _stablehlo.not: https://openxla.org/stablehlo/spec#not
  """
  return not_p.bind(x)


def bitwise_not(x: ArrayLike, /) -> Array:
  """Alias of :func:`jax.numpy.invert`."""
  return lax.bitwise_not(*promote_args('bitwise_not', x))

