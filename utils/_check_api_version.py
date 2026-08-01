
def _check_api_version(api_version: str | None) -> None:
    if api_version in _API_VERSIONS_OLD:
        warnings.warn(
            f"The {api_version} version of the array API specification was requested but the returned namespace is actually version 2025.12"
        )
    elif api_version is not None and api_version not in _API_VERSIONS:
        raise ValueError(
            "Only the 2025.12 version of the array API specification is currently supported"
        )

