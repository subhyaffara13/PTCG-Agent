from pathlib import Path


def caching_session(cache_dir: Path | None, *, use_pip: bool = False) -> requests.Session:
    """
    Return a `requests` style session, with suitable caching middleware.

    Uses the given `cache_dir` for the HTTP cache.

    `use_pip` determines how the fallback cache directory is determined, if `cache_dir` is None.
    When `use_pip` is `False`, `caching_session` will use a `pip-audit` internal cache directory.
    When `use_pip` is `True`, `caching_session` will attempt to discover `pip`'s cache
    directory, falling back on the internal `pip-audit` cache directory if the user's
    version of `pip` is too old.
    """

    # We limit the number of redirects to 5, since the services we connect to
    # should really never redirect more than once or twice.
    inner_session = requests.Session()
    inner_session.max_redirects = 5

    return CacheControl(
        inner_session,
        cache=_SafeFileCache(_get_cache_dir(cache_dir, use_pip=use_pip)),
    )

