
def with_fresh_cache_if_config() -> Generator[None, None, None]:
    if config.force_disable_caches:
        # Don't delete the cache dir because it has to survive beyond the
        # compile_fx call. Let's put the temp dirs under the default cache
        # dir so they're easier to locate.
        with fresh_cache(dir=cache_dir(), delete=False):
            yield
    else:
        yield

