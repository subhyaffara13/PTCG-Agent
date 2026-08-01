
def artificial_shared_memory_limit(limit):
    global _SMEM_SIZE_BOUND
    old_limit = _SMEM_SIZE_BOUND
    _SMEM_SIZE_BOUND = limit
    try:
        yield
    finally:
        _SMEM_SIZE_BOUND = old_limit

