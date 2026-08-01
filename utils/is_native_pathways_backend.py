
def is_native_pathways_backend() -> bool:
  return (
      hasattr(jax.devices()[0].client, 'pathways')
      or jax.devices()[0].client.runtime_type == 'pathways'
  )

