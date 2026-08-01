
def _get_cache_path():
    cache_dir = Path(mpl.get_cachedir(), 'test_cache')
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir

