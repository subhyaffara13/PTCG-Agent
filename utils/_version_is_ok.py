
def _version_is_ok() -> bool:
    _, version = _check_runtime_available()
    if check_native_version_skip() or (version in _CUTEDSL_REQUIRED_VERSIONS):
        return True

    log.warning(
        "cutedsl version %s is not known-good (ok: %s); "
        "set TORCH_NATIVE_SKIP_VERSION_CHECK=1 to override",
        version,
        _CUTEDSL_REQUIRED_VERSIONS,
    )
    return False

