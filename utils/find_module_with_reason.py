import time

def find_module_with_reason(id: str, manager: BuildManager) -> ModuleSearchResult:
    """Find a filesystem path for module `id` or the reason it can't be found."""
    if manager.stats_enabled:
        t0 = time.time()
    x = manager.find_module_cache.find_module(id, fast_path=False)
    if manager.stats_enabled:
        manager.add_stats(find_module_time=time.time() - t0, find_module_calls=1)
    return x

