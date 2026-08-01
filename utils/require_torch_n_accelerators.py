
def require_torch_n_accelerators(n: int):
    """Decorator marking a test that requires at least `n` accelerators (in PyTorch)."""

    def decorator(test_case):
        if not is_torch_available():
            return unittest.skip(reason="test requires PyTorch")(test_case)
        return unittest.skipUnless(backend_device_count(torch_device) >= n, f"test requires >= {n} accelerators")(
            test_case
        )

    return decorator

