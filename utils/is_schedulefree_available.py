
def is_schedulefree_available(min_version: str = SCHEDULEFREE_MIN_VERSION) -> bool:
    is_available, schedulefree_version = _is_package_available("schedulefree", return_version=True)
    return is_available and version.parse(schedulefree_version) >= version.parse(min_version)

