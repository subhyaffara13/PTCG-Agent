
def should_use_remote_dynamo_pgo_cache() -> bool:
    if torch.compiler.config.force_disable_caches:
        return False

    if (r := torch._dynamo.config.automatic_dynamic_remote_pgo) is not None:
        return r

    if not is_fbcode():
        return False

    if torch._utils_internal.is_fb_unit_test():
        return False

    try:
        from torch._inductor.fb.remote_cache import REMOTE_CACHE_VERSION
    except ModuleNotFoundError:
        return False

    return REMOTE_CACHE_VERSION >= torch._utils_internal.justknobs_getval_int(
        "pytorch/remote_cache:dynamo_pgo_version"
    )

