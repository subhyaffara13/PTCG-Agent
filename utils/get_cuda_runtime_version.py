
def get_cuda_runtime_version() -> tuple[int, int]:
    """Return the CUDA runtime version as (major, minor).

    Prefers a direct query of ``cudaRuntimeGetVersion`` via ``libcudart.so``. If that's
    not on the system loader path (common with pip-installed torch that bundles its own
    CUDA runtime), falls back to ``torch.version.cuda`` — which equals the bundled
    runtime's version for pip wheels. Returns ``(0, 0)`` for CPU-only torch.
    """
    import ctypes

    try:
        cudart = ctypes.CDLL("libcudart.so")
    except OSError:
        if not is_torch_available():
            return 0, 0
        import torch

        cuda_version = getattr(torch.version, "cuda", None)
        if cuda_version is None:
            return 0, 0

        major, minor, *_ = cuda_version.split(".")
        return int(major), int(minor)

    version = ctypes.c_int()
    cudart.cudaRuntimeGetVersion(ctypes.byref(version))
    return version.value // 1000, (version.value % 1000) // 10

