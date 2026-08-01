
def is_proxy_pathways_backend() -> bool:
  return jax.devices()[0].client.runtime_type == 'proxy/pathways'

