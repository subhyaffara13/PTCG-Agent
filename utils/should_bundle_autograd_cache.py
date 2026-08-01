
def should_bundle_autograd_cache() -> bool:
    return config.bundled_autograd_cache or torch._dynamo.config.caching_precompile

