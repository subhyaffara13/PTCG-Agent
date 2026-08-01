
def is_pathways_controller() -> bool:
  return jax.local_devices()[0].client.runtime_type == 'pathways'

