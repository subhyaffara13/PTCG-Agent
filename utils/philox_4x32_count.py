
def philox_4x32_count(key,
                      shape: Shape,
                      offset: typing.ArrayLike = 0,
                      fuse_output: bool = True):
  """Convenience function to call philox_4x32_kernel with padded shapes."""
  if len(shape) == 0:
    return philox_4x32_count(
        key, (1, 1), offset=offset, fuse_output=fuse_output)[..., 0, 0]
  elif len(shape) == 1:
    return philox_4x32_count(
        key, (1, *shape), offset=offset, fuse_output=fuse_output)[..., 0, :]

  requires_pad = (
      shape[-2] % BLOCK_SIZE[-2] != 0) or (shape[-1] % BLOCK_SIZE[-1] != 0)
  if requires_pad:
    padded_shape = tuple(shape[:-2]) + (
        prng_utils.round_up(shape[-2], BLOCK_SIZE[-2]),
        prng_utils.round_up(shape[-1], BLOCK_SIZE[-1]),
    )
    padded_result = philox_4x32_kernel(
        key, padded_shape, shape,
        block_size=BLOCK_SIZE, offset=offset,
        fuse_output=fuse_output)
    return padded_result[..., :shape[-2], :shape[-1]]
  else:
    return philox_4x32_kernel(key, shape, shape,
                              block_size=BLOCK_SIZE, offset=offset,
                              fuse_output=fuse_output)

