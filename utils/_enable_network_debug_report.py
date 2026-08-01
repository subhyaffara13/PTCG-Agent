
def _enable_network_debug_report(output_path: str | os.PathLike | None = None) -> None:
    _NETWORK_DEBUG_PROFILER.enable(output_path=output_path)

