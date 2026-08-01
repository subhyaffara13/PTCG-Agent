
def bitcast_convert_type(operand, dtype):
  operand = np.asarray(operand)
  nbits_in = dtypes.itemsize_bits(operand.dtype)
  nbits_out = dtypes.itemsize_bits(dtype)

  if nbits_out > nbits_in:
    assert operand.shape[-1] == nbits_out // nbits_in
    out_shape = operand.shape[:-1]
  elif nbits_out == nbits_in:
    out_shape = operand.shape
  else:
    out_shape = (*operand.shape, nbits_in // nbits_out)

  # Special handling for 4-bit integers.
  if nbits_in == 4:
    operand = _bitcast_uint4_to_uint8(operand.view('uint4'))
  if nbits_out == 4:
    operand = _bitcast_uint8_to_uint4(operand.view('uint8'))

  return operand.view(dtype).reshape(out_shape)


def bitcast_convert_type(operand: ArrayLike, new_dtype: DTypeLike) -> Array:
  """Elementwise bitcast.

  This function lowers directly to the `stablehlo.bitcast_convert`_ operation.

  The output shape depends on the size of the input and output dtypes with
  the following logic::

    if new_dtype.itemsize == operand.dtype.itemsize:
      output_shape = operand.shape
    if new_dtype.itemsize < operand.dtype.itemsize:
      output_shape = (*operand.shape, operand.dtype.itemsize // new_dtype.itemsize)
    if new_dtype.itemsize > operand.dtype.itemsize:
      assert operand.shape[-1] * operand.dtype.itemsize == new_dtype.itemsize
      output_shape = operand.shape[:-1]

  Args:
    operand: an array or scalar value to be cast
    new_dtype: the new type. Should be a NumPy type.

  Returns:
    An array of shape `output_shape` (see above) and type `new_dtype`,
    constructed from the same bits as operand.

  See also:
    - :func:`jax.lax.convert_element_type`: value-preserving dtype conversion.
    - :func:`jax.Array.view`: NumPy-style API for bitcast type conversion.

  .. _stablehlo.bitcast_convert: https://openxla.org/stablehlo/spec#bitcast_convert
  """
  new_dtype = dtypes.check_and_canonicalize_user_dtype(
      new_dtype, 'bitcast_convert_type')
  return bitcast_convert_type_p.bind(operand, new_dtype=new_dtype)

