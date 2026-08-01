
def _dev_env_hot_reload_enabled() -> bool:
    """The proxy exports this flag when started with ``--reload``. A reloaded
    worker is a fresh process that inherits the reloader's environment, so an
    edited ``.env`` value stays masked by the stale inherited one unless we
    let the file win; overriding makes the edit take effect on reload."""
    return os.getenv("LITELLM_DEV_ENV_HOT_RELOAD") == "True"

