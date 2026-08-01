
def _get_memory_metadata() -> str:
    """
    Get the current custom metadata that is being attached to CUDA memory allocations.

    Returns:
        str: The current metadata string, or empty string if no metadata is set.
    """
    # pyrefly: ignore [missing-attribute]
    return torch._C._cuda_getMemoryMetadata()

