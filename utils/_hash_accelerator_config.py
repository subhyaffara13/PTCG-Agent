
def _hash_accelerator_config(hash_obj, accelerators: np.ndarray):
  accelerator_devices = []
  for accelerator in accelerators.flat:
    accelerator_devices.append(accelerator)
  try:
    topology = xla_client.get_topology_for_devices(accelerator_devices)
    hash_obj.update(topology.fingerprint().to_bytes(8, byteorder="big"))
  except _jax.JaxRuntimeError as ex:
    # Fall back for those backends that do not support serialized
    # PjRtTopologyDescription as yet.
    logger.info("get (_hash_accelerator_config): unable to hash "
                "accelerator config, falling back to hashing "
                "devices %s (type %s)", ex, type(ex))
    _hash_devices(hash_obj, accelerators)

