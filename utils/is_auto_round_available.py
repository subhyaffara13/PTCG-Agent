
def is_auto_round_available(min_version: str = AUTOROUND_MIN_VERSION) -> bool:
    is_available, auto_round_version = _is_package_available("auto_round", return_version=True)
    return is_available and version.parse(auto_round_version) >= version.parse(min_version)

