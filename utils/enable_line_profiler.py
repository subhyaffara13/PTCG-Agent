
def enable_line_profiler() -> None:
    """Enable line_profiler for dynamic function wrapping.

    Raises:
        ImportError: If line_profiler is not available
    """
    global _line_profiler
    from line_profiler import LineProfiler  # Will raise ImportError if not available

    with _line_profiler_lock:
        if _line_profiler is None:
            _line_profiler = LineProfiler()
            verbose_proxy_logger.info("Line profiler enabled")

