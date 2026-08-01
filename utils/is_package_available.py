
def is_package_available(package_name: str) -> bool:
    return _get_version(package_name) != "N/A"

