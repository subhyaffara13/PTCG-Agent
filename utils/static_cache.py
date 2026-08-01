
def static_cache(static_cache: tp.MutableMapping[tp.Any, StaticCache]):
  if GRAPH_CONTEXT.caching:
    yield
    return

  GRAPH_CONTEXT.tmp_static_cache = static_cache

  try:
    yield
  finally:
    if GRAPH_CONTEXT.tmp_static_cache is not None:
      raise ValueError(
        'GRAPH_CONTEXT.tmp_static_cache should be None, no context consumed it.'
      )

