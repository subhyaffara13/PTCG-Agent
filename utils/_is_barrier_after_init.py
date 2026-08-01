
def _is_barrier_after_init() -> int:
    # Environment variable to control whether process group should perform a
    # barrier after its init. Default value is 0, i.e. no barrier. If you
    # experience issue with this setting, you may set
    # `TORCH_DIST_INIT_BARRIER=1` to add the barrier.
    return int(os.getenv("TORCH_DIST_INIT_BARRIER", "0"))

