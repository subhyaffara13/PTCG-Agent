
def combine_bias_and_mask(bias, mask, dtype):
  if bias is not None:
    # reshape bias to have 4D shape
    bias = bias.reshape((1,) * (4 - len(bias.shape)) + bias.shape)

  if mask is not None:
    if mask.dtype == np.dtype('bool'):
      large_negative_number = get_large_negative_number(dtype)
      mask = jnp.where(mask, jnp.asarray(0, dtype), large_negative_number)
    # reshape mask to have 4D shape
    mask = mask.reshape((1,) * (4 - len(mask.shape)) + mask.shape)

  # combine bias and mask
  if bias is None:
    bias = mask
  else:
    if mask is not None:
      # should be broadcast to same shape
      bias = bias + mask
  return bias

