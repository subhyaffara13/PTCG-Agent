
def is_compressed_tensors_available(min_version: str = COMPRESSED_TENSORS_MIN_VERSION) -> bool:
    is_available, compressed_tensors_version = _is_package_available("compressed_tensors", return_version=True)
    return is_available and version.parse(compressed_tensors_version) >= version.parse(min_version)

