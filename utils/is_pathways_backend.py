
def is_pathways_backend() -> bool:
  # Pathways is single-host.
  return is_native_pathways_backend() or is_proxy_pathways_backend()


def is_pathways_backend() -> bool:
  # Pathways is single-host.
  return (
      hasattr(jax.devices()[0].client, 'pathways')
      or jax.devices()[0].client.runtime_type == 'pathways'
      or jax.devices()[0].client.runtime_type == 'proxy/pathways'
  )

