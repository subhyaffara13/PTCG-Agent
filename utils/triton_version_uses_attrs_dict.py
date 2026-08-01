
def triton_version_uses_attrs_dict() -> bool:
    return get_triton_attrs_descriptor_version() == TritonAttrsDescriptorVersion.V4_DICT

