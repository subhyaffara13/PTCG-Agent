
def is_tpu() -> bool:
  return "TPU" in jax.devices()[0].device_kind

