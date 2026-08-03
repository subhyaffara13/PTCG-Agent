from typing import Optional

def collect_line_profiler_stats(output_file: Optional[str] = None) -> None:
    """Collect and save line_profiler statistics.

    This can be called manually to collect stats at any time, or it's
    automatically called on shutdown if register_shutdown_handler() was used.

    Args:
        output_file: Optional path to save stats. If None, prints to stdout.
    """
    global _line_profiler

    with _line_profiler_lock:
        if _line_profiler is None:
            verbose_proxy_logger.debug("Line profiler not enabled, nothing to collect")
            return

        try:
            if output_file:
                # Save to file
                output_path = PathLib(output_file)
                _line_profiler.dump_stats(str(output_path))
                verbose_proxy_logger.info(f"Line profiler stats saved to {output_path}")
            else:
                # Print to stdout
                from io import StringIO

                stream = StringIO()
                _line_profiler.print_stats(stream=stream)
                stats_output = stream.getvalue()
                verbose_proxy_logger.info("Line profiler stats:\n" + stats_output)
        except Exception as e:
            verbose_proxy_logger.error(f"Error collecting line profiler stats: {e}")

