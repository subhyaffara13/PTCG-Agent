
def is_gguf_available(min_version: str = GGUF_MIN_VERSION) -> bool:
    is_available, gguf_version = _is_package_available("gguf", return_version=True)
    return is_available and version.parse(gguf_version) >= version.parse(min_version)

