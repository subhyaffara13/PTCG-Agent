
def is_huggingface_hub_greater_or_equal(library_version: str, accept_dev: bool = False) -> bool:
    is_available, hub_version = _is_package_available("huggingface_hub", return_version=True)
    if not is_available:
        return False

    if accept_dev:
        return version.parse(version.parse(hub_version).base_version) >= version.parse(library_version)
    else:
        return version.parse(hub_version) >= version.parse(library_version)

