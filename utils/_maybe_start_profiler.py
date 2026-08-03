from typing import Any

def _maybe_start_profiler(should_profile: bool) -> Any:
    if should_profile:
        import pyinstrument  # type: ignore[import-not-found]

        profiler = pyinstrument.Profiler(async_mode="disabled")
        profiler.start()
        return profiler
    return None

