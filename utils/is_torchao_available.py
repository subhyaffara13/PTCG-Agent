
def is_torchao_available(min_version: str = TORCHAO_MIN_VERSION) -> bool:
    if not is_torch_available():
        return False
    is_available, torchao_version = _is_package_available("torchao", return_version=True)
    return is_available and version.parse(torchao_version) >= version.parse(min_version)

