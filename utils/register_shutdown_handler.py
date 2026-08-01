
def register_shutdown_handler(output_file: Optional[str] = None) -> None:
    """Register a shutdown handler to collect line_profiler stats.

    This registers an atexit handler that will automatically save profiling
    statistics when the Python process exits. Safe to call multiple times
    (only registers once).

    Args:
        output_file: Optional path to save stats on shutdown.
                     Defaults to 'line_profile_stats.lprof'
    """
    if output_file is None:
        output_file = "line_profile_stats.lprof"

    def shutdown_handler():
        collect_line_profiler_stats(output_file=output_file)

    atexit.register(shutdown_handler)
    verbose_proxy_logger.debug(
        f"Registered line_profiler shutdown handler for {output_file}"
    )

