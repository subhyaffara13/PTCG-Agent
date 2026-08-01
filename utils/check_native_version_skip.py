
def check_native_version_skip() -> bool:
    """
    Single point to check if native DSL version gating should be skipped,
    checked via:
    TORCH_NATIVE_SKIP_VERSION_CHECK=1
    """
    return int(os.getenv("TORCH_NATIVE_SKIP_VERSION_CHECK", 0)) == 1

