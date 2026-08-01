
def require_large_cpu_ram(test_case, memory: float = 80):
    """Decorator marking a test that requires a CPU RAM with more than `memory` GiB of memory."""
    if not is_psutil_available():
        return test_case

    import psutil

    return unittest.skipUnless(
        psutil.virtual_memory().total / 1024**3 > memory,
        f"test requires a machine with more than {memory} GiB of CPU RAM memory",
    )(test_case)

