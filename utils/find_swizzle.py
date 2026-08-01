
def find_swizzle(minor_dim_bits: int, what: str = ""):
  """Returns the largest swizzle that can be applied to a memory region.

  Swizzling is usually necessary when dealing with 2D data in SMEM, especially
  if the reference is used as an MMA operand. The returned swizzle is usually
  applied as ``plgpu`` transform:

    transforms = (
        plgpu.TilingTransform((8, 8 * swizzle // elem_bits)),
        plgpu.SwizzleTransform(swizzle))
    )

  Args:
    minor_dim_bits: The number of bits in the minor (last) dimension of the
      memory region. Usually computed as ``dim_size * jnp.finfo(dtype).bits``.
    what: A string describing the operand for which the swizzle is being
      computed. Improves the error message if specified.
  """
  for swizzle_bytes in (128, 64, 32, 16):
    if minor_dim_bits % (swizzle_bytes * 8) == 0:
      return swizzle_bytes
  if what:
    what = " for " + what
  raise ValueError(
      f"No valid out swizzle{what}: minor dimension has"
      f" {minor_dim_bits} bits, which is not a multiple of 128 (16 bytes)"
  )

