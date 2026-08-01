
def is_fsdp_available(min_version: str = FSDP_MIN_VERSION) -> bool:
    return is_torch_available() and version.parse(get_torch_version()) >= version.parse(min_version)

