from typing import Any

def _get_network_debug_report() -> dict[str, Any]:
    return _NETWORK_DEBUG_PROFILER.build_report()

