
def find_module_simple(id: str, manager: BuildManager) -> str | None:
    """Find a filesystem path for module `id` or `None` if not found."""
    if manager.stats_enabled:
        t0 = time.time()
    x = manager.find_module_cache.find_module(id, fast_path=True)
    if manager.stats_enabled:
        manager.add_stats(find_module_time=time.time() - t0, find_module_calls=1)
    if isinstance(x, ModuleNotFoundReason):
        return None
    return x

