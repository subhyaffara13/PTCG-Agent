
def convert_element_type(g: jit_utils.GraphContext, self, *args):
    dtype = symbolic_helper._get_const(args[0], "i", "dtype")
    return g.op("Cast", self, to_i=_type_utils.JitScalarType(dtype).onnx_type())


def convert_element_type(input: torch.Tensor, dtype: torch.dtype) -> torch.Tensor:
    return torch.ops.prims.convert_element_type.default(input, dtype)


def convert_element_type(operand, dtype):
  return np.asarray(operand, dtype=dtype)


def convert_element_type(operand: ArrayLike,
                         new_dtype: DTypeLike | dtypes.ExtendedDType) -> Array:
  """Elementwise cast.

  This function lowers directly to the `stablehlo.convert`_ operation, which
  performs an elementwise conversion from one type to another, similar to a
  C++ ``static_cast``.

  Args:
    operand: an array or scalar value to be cast.
    new_dtype: a dtype-like object (e.g. a :class:`numpy.dtype`, a scalar type,
      or a valid dtype name) representing the target dtype.

  Returns:
    An array with the same shape as ``operand``, cast elementwise to ``new_dtype``.

  .. note::

     If ``new_dtype`` is a 64-bit type and `x64 mode`_ is not enabled,
     the appropriate 32-bit type will be used in its place.

     If the input is a JAX array and the input dtype and output dtype match, then
     the input array will be returned unmodified.

  See also:
    - :func:`jax.numpy.astype`: NumPy-style dtype casting API.
    - :meth:`jax.Array.astype`: dtype casting as an array method.
    - :func:`jax.lax.bitcast_convert_type`: cast bits directly to a new dtype.

  .. _stablehlo.convert: https://openxla.org/stablehlo/spec#convert
  .. _x64 mode: https://docs.jax.dev/en/latest/notebooks/Common_Gotchas_in_JAX.html#double-64bit-precision
  """
  new_dtype = dtypes.check_and_canonicalize_user_dtype(
      new_dtype, 'convert_element_type')
  return _convert_element_type(operand, new_dtype, weak_type=False)

