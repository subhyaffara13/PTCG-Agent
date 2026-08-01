
def _storage_type_to_dtype_map():
    dtype_map = {val: key for key, val in _dtype_to_storage_type_map().items()}
    return dtype_map

