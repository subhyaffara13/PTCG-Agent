
def clear_all_caches():
  for cache in list(_caches.keys()):
    cache.cache_clear()

