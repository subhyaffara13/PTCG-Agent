
def deserialize_storage_offset(offset: SymInt) -> int:
    if offset.type != "as_int":
        raise AssertionError(f"Only as_int is supported, got {offset.type}")
    return offset.as_int

