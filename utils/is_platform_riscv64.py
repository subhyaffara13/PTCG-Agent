
def is_platform_riscv64() -> bool:
    """
    Checking if the running platform use riscv64 architecture.

    Returns
    -------
    bool
        True if the running platform uses riscv64 architecture.
    """
    return platform.machine() == "riscv64"

