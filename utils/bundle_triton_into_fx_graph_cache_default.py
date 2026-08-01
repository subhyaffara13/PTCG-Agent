
def bundle_triton_into_fx_graph_cache_default() -> bool | None:
    return get_tristate_env(
        "TORCHINDUCTOR_BUNDLE_TRITON_INTO_FX_GRAPH_CACHE",
        True if not is_fbcode() else None,
    )

