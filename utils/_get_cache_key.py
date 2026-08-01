
def _get_cache_key(
    *,
    edge_attrs,
    node_attrs,
    preserve_edge_attrs,
    preserve_node_attrs,
    preserve_graph_attrs,
):
    """Return key used by networkx caching given arguments for ``convert_from_nx``."""
    # edge_attrs: dict | None
    # node_attrs: dict | None
    # preserve_edge_attrs: bool (False if edge_attrs is not None)
    # preserve_node_attrs: bool (False if node_attrs is not None)
    return (
        frozenset(edge_attrs.items())
        if edge_attrs is not None
        else preserve_edge_attrs,
        frozenset(node_attrs.items())
        if node_attrs is not None
        else preserve_node_attrs,
    )


def _get_cache_key(
    options: xc.CompileOptions,
    backend: xc.Client,
    computation: ir.Module,
    devices: np.ndarray,
    override_fdo_profile: bytes | None = None) -> str | None:
  if not compilation_cache.is_cache_used(backend):
    return None
  if config.remove_custom_partitioning_ptr_from_cache_key.value:
    ignore_callbacks = cache_key_type.IgnoreCallbacks.CUSTOM_PARTITIONING
  else:
    ignore_callbacks = cache_key_type.IgnoreCallbacks.NO
  if override_fdo_profile is not None:
    options = copy.deepcopy(options)
    options.executable_build_options.fdo_profile = override_fdo_profile
  try:
    return compilation_cache.get_cache_key(
        computation,
        devices,
        options,
        backend,
        ignore_callbacks,
    )
  except _jax.JaxRuntimeError as ex:
    logger.error("compile_or_get_cached: unable to generate cache key, "
                  "skipping the cache: %s", ex)
  return None

