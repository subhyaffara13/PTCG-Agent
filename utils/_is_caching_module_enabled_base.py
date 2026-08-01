
def _is_caching_module_enabled_base() -> bool:
    """Base check for caching module enablement via versioned config."""
    return _versioned_config(
        _CACHING_MODULE_VERSION_JK,
        _CACHING_MODULE_VERSION,
        _CACHING_MODULE_OSS_DEFAULT,
        _CACHING_MODULE_ENV_VAR_OVERRIDE,
    )

