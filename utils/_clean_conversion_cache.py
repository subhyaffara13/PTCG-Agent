from pathlib import Path


def _clean_conversion_cache():
    # This will actually ignore mpl_toolkits baseline images, but they're
    # relatively small.
    baseline_images_size = sum(
        path.stat().st_size
        for path in Path(mpl.__file__).parent.glob("**/baseline_images/**/*"))
    # 2x: one full copy of baselines, and one full copy of test results
    # (actually an overestimate: we don't convert png baselines and results).
    max_cache_size = 2 * baseline_images_size
    # Reduce cache until it fits.
    with cbook._lock_path(_get_cache_path()):
        cache_stat = {
            path: path.stat() for path in _get_cache_path().glob("*")}
        cache_size = sum(stat.st_size for stat in cache_stat.values())
        paths_by_atime = sorted(  # Oldest at the end.
            cache_stat, key=lambda path: cache_stat[path].st_atime,
            reverse=True)
        while cache_size > max_cache_size:
            path = paths_by_atime.pop()
            cache_size -= cache_stat[path].st_size
            path.unlink()

