import os

def check_native_jit_disabled() -> bool:
    """
    Single point to check if native DSL ops are disabled globally,
    checked via:
    TORCH_DISABLE_NATIVE_JIT=1
    """
    return int(os.getenv("TORCH_DISABLE_NATIVE_JIT", 0)) == 1

