
def autotune_remote_cache_default() -> bool | None:
    return get_tristate_env("TORCHINDUCTOR_AUTOTUNE_REMOTE_CACHE")

