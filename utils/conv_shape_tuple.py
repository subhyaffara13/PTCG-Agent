
def conv_shape_tuple(lhs_shape, rhs_shape, strides, pads, batch_group_count=1):
  """Compute the shape tuple of a conv given input shapes in canonical order."""
  if isinstance(pads, str):
    pads = lax.padtype_to_pads(lhs_shape[2:], rhs_shape[2:], strides, pads)
  if len(pads) != len(lhs_shape) - 2:
    msg = "Wrong number of explicit pads for convolution: expected {}, got {}."
    raise TypeError(msg.format(len(lhs_shape) - 2, len(pads)))

  lhs_padded = np.add(lhs_shape[2:], np.sum(np.array(pads).reshape(-1, 2),
                                              axis=1))
  if np.any(lhs_padded < 0):
    raise ValueError("Negative padding is larger than the size of the corresponding dimension: "
                     f"got padding={pads} for lhs_shape[2:]={lhs_shape[2:]}")
  out_space = tuple(map(core.stride_dim, lhs_padded, rhs_shape[2:], strides))
  if batch_group_count > 1:
    assert lhs_shape[0] % batch_group_count == 0
    out_shape_0 = lhs_shape[0] // batch_group_count
  else:
    out_shape_0 = lhs_shape[0]
  out_shape = (out_shape_0, rhs_shape[0])
  return tuple(out_shape + tuple(out_space))

