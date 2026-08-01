
def _validate_default_device(val):
  if (val is not None and
      not isinstance(val, xla_client.Device) and
      val not in ['cpu', 'gpu', 'tpu']):
    # TODO(skyewm): this is a workaround for non-PJRT Device types. Remove when
    # all JAX backends use a single C++ device interface.
    if 'Device' in str(type(val)):
      logger.info(
          'Allowing non-`xla_client.Device` default device: %s, type: %s',
          repr(val), type(val))
      return
    raise ValueError('jax.default_device must be passed either a Device object (e.g. '
                     f"`jax.devices('cpu')[0]`) or a platform name string like 'cpu' or 'gpu'"
                     f", got: {val!r}")

