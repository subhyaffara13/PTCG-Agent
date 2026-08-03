import os

def get_rocm_compiler() -> str:
    """
    Get path to ROCm's clang compiler.
    Uses PyTorch's ROCM_HOME detection.

    Returns:
        Path to clang compiler

    Raises:
        RuntimeError: If ROCm is not found
    """
    if ROCM_HOME is None:
        raise RuntimeError(
            "ROCm installation not found. "
            "PyTorch was not built with ROCm support or ROCM_HOME is not set."
        )

    # ROCm's clang is at <ROCM_HOME>/llvm/bin/clang
    clang_path = _join_rocm_home("llvm", "bin", "clang")

    if not os.path.exists(clang_path):
        raise RuntimeError(
            f"ROCm clang not found at {clang_path}. ROCM_HOME is set to {ROCM_HOME}"
        )

    return clang_path

