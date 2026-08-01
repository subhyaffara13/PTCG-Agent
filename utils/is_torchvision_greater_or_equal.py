
def is_torchvision_greater_or_equal(library_version: str) -> bool:
    if not is_torchvision_available():
        return False
    _, torchvision_version = _is_package_available("torchvision", return_version=True)
    return version.parse(torchvision_version) >= version.parse(library_version)

