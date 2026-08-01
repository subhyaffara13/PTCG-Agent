
def requires_accelerator_dist_backend(backends=None):
    """
    Decorator to skip tests if no accelerator communication backend (NCCL, XCCL, HCCL) is available.

    Args:
        backends (Optional[List[str]]): Specific accelerator backends to check (e.g., ["nccl", "xccl", "hccl"]).
                                       If None, checks all supported accelerator backends (NCCL, XCCL, HCCL).

    Returns:
        callable: A decorator that skips the test if no specified accelerator backend is available.
    """
    if backends is None:
        backends = ACCELERATOR_DIST_BACKENDS

    backend_available = any(
        {
            "nccl": c10d.is_nccl_available,
            "xccl": c10d.is_xccl_available,
            "hccl": lambda: TEST_HPU,
        }.get(backend, lambda: False)()
        for backend in backends
    )

    return skip_but_pass_in_sandcastle_if(
        not backend_available,
        f"No accelerator communication backend available among {backends}",
    )

