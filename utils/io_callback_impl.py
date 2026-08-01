
def io_callback_impl(
    *args,
    result_avals,
    callback: _FlatCallback,
    sharding: Sharding | None,
    ordered: bool,
):
  del result_avals, sharding, ordered
  try:
    cpu_device, *_ = xb.local_devices(backend="cpu")
  except RuntimeError as e:
    raise RuntimeError(
        "jax.io_callback failed to find a local CPU device to place the"
        " inputs on. Make sure \"cpu\" is listed in --jax_platforms or the"
        " JAX_PLATFORMS environment variable."
    ) from e
  args = api.device_put(args, cpu_device)
  with config.default_device(cpu_device):
    try:
      return tree_util.tree_map(np.asarray, callback(*args))
    except BaseException:
      logger.exception("jax.io_callback failed")
      raise

