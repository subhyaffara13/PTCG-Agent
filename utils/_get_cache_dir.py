
def _get_cache_dir(custom_cache_dir: Path | None, *, use_pip: bool = True) -> Path:
    """
    Returns a directory path suitable for HTTP caching.

    The directory is **not** guaranteed to exist.

    `use_pip` tells the function to prefer `pip`'s pre-existing cache,
    **unless** `PIP_NO_CACHE_DIR` is present in the environment.
    """

    # If the user has explicitly requested a directory, pass it through unscathed.
    if custom_cache_dir is not None:
        return custom_cache_dir

    # Retrieve pip-audit's default internal cache using `platformdirs`.
    pip_audit_cache_dir = user_cache_path("pip-audit", appauthor=False, ensure_exists=True)

    # If the retrieved cache isn't the legacy one, try to delete the old cache if it exists.
    if (
        _PIP_AUDIT_LEGACY_INTERNAL_CACHE.exists()
        and pip_audit_cache_dir != _PIP_AUDIT_LEGACY_INTERNAL_CACHE
    ):
        shutil.rmtree(_PIP_AUDIT_LEGACY_INTERNAL_CACHE)

    # Respect pip's PIP_NO_CACHE_DIR environment setting.
    if use_pip and not os.getenv("PIP_NO_CACHE_DIR"):
        pip_cache_dir = _get_pip_cache() if _PIP_VERSION >= _MINIMUM_PIP_VERSION else None
        if pip_cache_dir is not None:
            return pip_cache_dir
        else:
            logger.warning(
                f"pip {_PIP_VERSION} doesn't support the `cache dir` subcommand, "
                f"using {pip_audit_cache_dir} instead"
            )
            return pip_audit_cache_dir
    else:
        return pip_audit_cache_dir


def _get_cache_dir() -> str:
    """Locate a platform-appropriate cache directory to use.

    Does not ensure that the cache directory exists.
    """
    # Linux, Unix, AIX, etc.
    if os.name == 'posix' and sys.platform != 'darwin':
        # use ~/.cache if empty OR not set
        base_path = os.environ.get('XDG_CACHE_HOME') or os.path.expanduser(
            '~/.cache'
        )
        return os.path.join(base_path, 'python-entrypoints')

    # Mac OS
    elif sys.platform == 'darwin':
        return os.path.expanduser('~/Library/Caches/Python Entry Points')

    # Windows (hopefully)
    else:
        base_path = os.environ.get('LOCALAPPDATA') or os.path.expanduser(
            '~\\AppData\\Local'
        )
        return os.path.join(base_path, 'Python Entry Points')


def _get_cache_dir(
    req: InstallRequirement,
    wheel_cache: WheelCache,
) -> str:
    """Return the persistent or temporary cache directory where the built
    wheel need to be stored.
    """
    cache_available = bool(wheel_cache.cache_dir)
    assert req.link
    if cache_available and _should_cache(req):
        cache_dir = wheel_cache.get_path_for_link(req.link)
    else:
        cache_dir = wheel_cache.get_ephem_path_for_link(req.link)
    return cache_dir

