
def _check_sharding(aval, s):
  if (s is not None and
      not isinstance(s, (xc.Device, Sharding, Format, core.MemorySpace))):
    raise ValueError(
        "`jax.device_put` only accepts `None`, `jax.sharding.Sharding`,"
        " `jax.Device`, `Format`, `jax.memory.Space` or a pytree of these"
        f" values. Received invalid value: {s}")
  if isinstance(aval, core.ShapedArray) and aval.dtype == dtypes.string_dtype:
    _check_string_compatible_sharding(s)

  if isinstance(s, Sharding):
    if isinstance(aval, core.AbstractToken):
      aval = core.get_token_aval()
    pjit.pjit_check_aval_sharding(
        (s,), (aval,), ("",), "device_put args", allow_uneven_sharding=False
    )
    s.shard_shape(aval.shape)  # should raise an Error if incompatible


def _check_sharding(sharding, shape):
  if sharding is None:
    return
  if isinstance(sharding, P):
    sharding._check_compatible_wrt_shape(shape)
  else:
    sharding.check_compatible_aval(shape)


def _check_sharding(x):
  if hasattr(jax, "Array") and isinstance(x, jax.Array):
    if not jax.typeof(x).sharding.is_fully_replicated:
      return True
    else:
      return len(x.sharding.device_set) > 1
  # pytype: disable=attribute-error
  return (
      hasattr(jax, "pxla")
      and hasattr(jax.pxla, "ShardedDeviceArray")
      and isinstance(x, jax.pxla.ShardedDeviceArray)
  )

