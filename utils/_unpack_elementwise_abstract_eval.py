
def _unpack_elementwise_abstract_eval(
    x, *, index, packed_dtype, unpacked_dtype
):
  if dtypes.itemsize_bits(x.dtype) != dtypes.itemsize_bits(unpacked_dtype):
    raise ValueError(
        "The bitwidth of `x` must match the bitwidth of `unpacked_dtype` for "
        f"unpack_elementwise, but got {x.dtype} and {unpacked_dtype}"
    )
  packing_factor = _get_elementwise_packing_factor(unpacked_dtype, packed_dtype)
  if index < 0 or index >= packing_factor:
    raise ValueError(
        f"Index {index} is out of bounds for packing factor {packing_factor}")
  return jax_core.ShapedArray(x.shape, unpacked_dtype)

