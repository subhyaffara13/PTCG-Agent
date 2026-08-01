
def debug_callback_impl(*args, callback: Callable[..., Any],
                        effect: DebugEffect, partitioned: bool):
  del effect, partitioned
  try:
    cpu_device, *_ = xla_bridge.local_devices(backend="cpu")
  except RuntimeError as e:
    raise RuntimeError(
        "jax.debug.callback failed to find a local CPU device to place the"
        " inputs on. Make sure \"cpu\" is listed in --jax_platforms or the"
        " JAX_PLATFORMS environment variable."
    ) from e
  args = api.device_put(args, cpu_device)
  with (config.default_device(cpu_device),
        sharding_impls._internal_use_concrete_mesh(mesh_lib.empty_concrete_mesh),
        mesh_lib.use_abstract_mesh(mesh_lib.empty_abstract_mesh)):
    try:
      callback(*args)
    except BaseException:
      logger.exception("jax.debug.callback failed")
      raise
  return ()

