
def inductor_meta_from_config() -> _InductorMetaTy:
    from torch._inductor import config

    backend_hash = None
    if has_triton():
        try:
            backend_hash = torch.utils._triton.triton_hash_with_backend()
        except RuntimeError:
            # This can get the error:
            #   RuntimeError: 0 active drivers ([]). There should only be one.
            pass

    is_hip = None
    if torch.version.hip is not None:
        is_hip = True

    return {
        "autotune_local_cache": config.autotune_local_cache,
        "autotune_remote_cache": config.autotune_remote_cache,
        "backend_hash": backend_hash,
        "bundled_autotune_remote_cache": config.bundled_autotune_remote_cache,
        "coordinate_descent_tuning": config.coordinate_descent_tuning,
        "is_fbcode": config.is_fbcode(),
        "is_hip": is_hip,
    }

