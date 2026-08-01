
def get_sync_debug_mode() -> int:
    r"""Return current value of debug mode for cuda synchronizing operations."""
    _lazy_init()
    return torch._C._cuda_get_sync_debug_mode()

