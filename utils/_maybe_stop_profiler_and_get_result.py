
def _maybe_stop_profiler_and_get_result(profiler) -> str | None:
    if profiler is None:
        return None
    profiler.stop()
    return profiler.output_text(unicode=True)

