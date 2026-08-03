import logging

def build_cpu_memory_monitor(logger_instance: logging.Logger | None = None) -> CPUMemoryMonitor:
    """Build and initialize a CPU memory monitor.

    Args:
        logger_instance: Optional logger to log initialization info. If None, no logging is done.

    Returns:
        CPUMemoryMonitor instance.
    """
    monitor = CPUMemoryMonitor()
    if logger_instance is not None:
        if is_psutil_available():
            logger_instance.info(f"CPU memory monitor initialized: {monitor.total_memory_gib:.2f} GiB total")
        else:
            logger_instance.warning("psutil not available, memory monitoring disabled")
    return monitor

