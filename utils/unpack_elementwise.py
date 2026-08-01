
def unpack_elementwise(output: _ods_ir.Type, source: _ods_ir.Value[_ods_ir.VectorType], source_type: _Union[_ods_ir.Type, _ods_ir.TypeAttr], index: _Union[int, _ods_ir.IntegerAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return UnpackElementwiseOp(output=output, source=source, source_type=source_type, index=index, loc=loc, ip=ip).result


def unpack_elementwise(x, *, index, packed_dtype, unpacked_dtype):
  """Unpacks an elementwise packed array.

  The function follows the *interleaved format* during unpacking, and it's the
  reverse of `pack_elementwise`.

  For example, if `packed_dtype` is `int4`, `unpacked_dtype` is `int8`,
  and `x` is packed `int8` with x'y'z'w'm'n'i'j' in a word, where each
  character represents 4 bits:

  When `index=0`, the result is a packed i8 with s_y'y's_w'w's_n'n's_j'j';
  When `index=1`, the result is a packed i8 with s_x'x's_z'z's_m'm's_i'i'.
  With `s_x` indicating the MSB of `x`, and so on.

  For logical array, this unpacking results in a strided access pattern.
  For example, if a 2D logical array `x` is packed as `int8` and unpacked to
  `int16`, then

  ```python
  i8_x = pltpu.bitcast(i16_x, jnp.int8)
  y = unpack_elementwise(
      i16_x, index=0, packed_dtype=jnp.int8, unpacked_dtype=jnp.int16)
  z = unpack_elementwise(
      i16_x, index=1, packed_dtype=jnp.int8, unpacked_dtype=jnp.int16)
  np.testing.assert_array_equal(y, i8_x[0::2, :].astype(jnp.int16))
  np.testing.assert_array_equal(z, i8_x[1::2, :].astype(jnp.int16))
  ```

  Args:
    x: The packed array.
    index: The index of the element to unpack.
    packed_dtype: Elements
    unpacked_dtype: The dtype of the unpacked array.

  Returns:
    The unpacked array in `unpacked_dtype`.
  """
  return unpack_elementwise_p.bind(
      x, index=index, packed_dtype=packed_dtype, unpacked_dtype=unpacked_dtype
  )

