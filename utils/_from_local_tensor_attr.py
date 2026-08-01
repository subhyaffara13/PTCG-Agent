
def _from_local_tensor_attr(attr: str) -> int:
    if not _is_local_tensor_attr(attr):
        raise AssertionError(f"Invalid local tensor attr {attr}")
    return int(attr[len(_LOCAL_TENSOR_ATTR_PREFIX) :])

