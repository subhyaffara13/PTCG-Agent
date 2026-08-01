
def get_concrete_mesh() -> Mesh:
  val = jax_config.device_context.value
  return empty_concrete_mesh if val is None else val

