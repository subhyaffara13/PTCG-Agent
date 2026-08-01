
def bundled_autotune_remote_cache_default() -> bool | None:
    return get_tristate_env("TORCHINDUCTOR_BUNDLED_AUTOTUNE_REMOTE_CACHE")

