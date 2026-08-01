
def is_default_layout(curr_layout, sharding, aval):
  if curr_layout is None or sharding is None or isinstance(sharding, UnspecifiedValue):
    return True
  if (aval is core.abstract_token or aval.dtype == dtypes.float0 or
      dtypes.issubdtype(aval.dtype, dtypes.extended)):
    return True
  if isinstance(curr_layout, AutoLayoutSingleton):
    return False
  d = sharding._device_assignment[0]
  shard_shape = sharding.shard_shape(aval.shape)
  try:
    # TODO(yashkatariya): Replace this with normal `==` check once CPU supports
    # int4.
    return is_user_xla_layout_equal(
        curr_layout,
        Layout.from_pjrt_layout(
            d.client.get_default_layout(aval.dtype, shard_shape, d)))
  except _jax.JaxRuntimeError as e:
    msg, *_ = e.args
    if isinstance(msg, str) and msg.startswith("UNIMPLEMENTED"):
      return True
    else:
      raise

