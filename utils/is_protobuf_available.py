
def is_protobuf_available() -> bool:
    return _is_package_available("google")[0] and _is_package_available("google.protobuf")[0]

