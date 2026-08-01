
def _get_elementwise_packing_factor(unpacked_dtype, packed_dtype):
  unpacked_bitwidth = dtypes.itemsize_bits(unpacked_dtype)
  packed_bitwidth = dtypes.itemsize_bits(packed_dtype)
  if unpacked_bitwidth % packed_bitwidth != 0:
    raise ValueError(
        "Unpacked bitwidth must be a multiple of packed bitwidth, got "
        f"{unpacked_bitwidth} and {packed_bitwidth}"
    )
  return unpacked_bitwidth // packed_bitwidth

