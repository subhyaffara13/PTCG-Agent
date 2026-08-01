
def should_use_local_autograd_cache() -> bool:
    if torch.compiler.config.force_disable_caches:
        return False
    return config.enable_autograd_cache

