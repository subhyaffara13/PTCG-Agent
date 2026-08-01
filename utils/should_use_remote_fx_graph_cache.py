
def should_use_remote_fx_graph_cache() -> bool:
    if config.fx_graph_remote_cache is not None:
        return config.fx_graph_remote_cache
    if not config.is_fbcode():
        return False

    if torch._utils_internal.is_fb_unit_test():
        return False

    try:
        from torch._inductor.fb.remote_cache import REMOTE_CACHE_VERSION
    except ModuleNotFoundError:
        return False

    return REMOTE_CACHE_VERSION >= torch._utils_internal.justknobs_getval_int(
        "pytorch/remote_cache:fx_graph_memcache_version"
    )

