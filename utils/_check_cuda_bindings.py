from typing import Any

def _check_cuda_bindings(result: Any) -> Any:
    """Check a cuda.bindings (cuda-python) call result for errors.

    All cuda.bindings runtime calls return ``(error, *outputs)``.  This
    helper unpacks the tuple, raises on non-success, and returns the
    outputs (``None`` for zero outputs, scalar for one, tuple otherwise).
    """
    if not _HAS_CUDA_BINDINGS:
        raise RuntimeError("cuda.bindings is not available")
    err, *out = result
    if (
        err
        != _cuda_bindings_runtime.cudaError_t.cudaSuccess  # pyrefly: ignore[missing-attribute]
    ):
        _, err_str = (
            _cuda_bindings_runtime.cudaGetErrorString(  # pyrefly: ignore[missing-attribute]
                err
            )
        )
        if isinstance(err_str, bytes):
            err_str = err_str.decode()
        raise RuntimeError(f"CUDA error: {err} ({err_str})")
    if len(out) == 0:
        return None
    if len(out) == 1:
        return out[0]
    return out

