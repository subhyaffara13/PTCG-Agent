
def extract_tensor_metadata_for_cache_key(t: Tensor) -> TensorMetadata:
    """
    Extracts the tensor metadata and removes fields of the TensorMetadata
    that are not needed for caching
    """
    meta = extract_tensor_metadata(t)
    if not hasattr(t, "_is_inductor_static"):
        meta = dataclasses.replace(meta, storage_offset=0, storage_bytes=None)

    return meta

