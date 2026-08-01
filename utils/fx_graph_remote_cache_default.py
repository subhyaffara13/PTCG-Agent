
def fx_graph_remote_cache_default() -> bool | None:
    return get_tristate_env("TORCHINDUCTOR_FX_GRAPH_REMOTE_CACHE")

