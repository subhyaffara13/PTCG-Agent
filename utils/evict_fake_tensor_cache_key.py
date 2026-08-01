
def evict_fake_tensor_cache_key(key: _DispatchCacheKey) -> None:
    if key in FakeTensorMode.cache:
        FakeTensorMode.cache.pop(key)

