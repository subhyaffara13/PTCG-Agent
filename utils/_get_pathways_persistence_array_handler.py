
def _get_pathways_persistence_array_handler(
    **kwargs,
) -> type_handlers.ArrayHandler:
  """Returns the Pathways persistence array handler."""
  if multihost.is_proxy_pathways_backend():
    logging.info('Using CloudPathwaysArrayHandler for jax.Array.')
    return cloud_pathways_array_handler.CloudPathwaysArrayHandler(**kwargs)

  raise NotImplementedError(
      'Pathways persistence array handler is not supported on this backend.'
  )

