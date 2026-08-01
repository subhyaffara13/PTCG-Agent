
def _should_use_implicit_mempool() -> bool:
    r"""
    Check if the implicit memory pool should be used for symmetric memory allocations.

    Returns:
        bool: True if the implicit memory pool should be used, False otherwise.

    By default, use implicit memory pool for `symm_mem.empty`.  Users can
    disable this by setting the environment variable `TORCH_SYMMMEM_IMPLICIT_POOL` to `0`.
    """
    global _use_implicit_mempool
    if _use_implicit_mempool is None:
        _use_implicit_mempool = os.getenv("TORCH_SYMMMEM_IMPLICIT_POOL", "1") == "1"

    return _use_implicit_mempool

