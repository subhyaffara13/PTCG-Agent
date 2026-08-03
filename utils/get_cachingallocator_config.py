import os

def get_cachingallocator_config() -> _Dict[str, str]:
    """Return the caching allocator configuration from environment variables.
    """
    # pyrefly: ignore [bad-return]
    return {
        var: os.environ.get(var)
        for var in (
            "PYTORCH_CUDA_ALLOC_CONF",
            "PYTORCH_HIP_ALLOC_CONF",
            "PYTORCH_ALLOC_CONF",
        )
        if os.environ.get(var)
    }

