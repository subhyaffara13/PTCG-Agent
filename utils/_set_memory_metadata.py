
def _set_memory_metadata(metadata: str):
    """
    Set custom metadata that will be attached to all subsequent CUDA memory allocations.

    This metadata will be recorded in the memory snapshot for all allocations made
    after this call until the metadata is cleared or changed.

    Args:
        metadata (str): Custom metadata string to attach to allocations.
                       Pass an empty string to clear the metadata.
    """
    # pyrefly: ignore [missing-attribute]
    torch._C._cuda_setMemoryMetadata(metadata)

