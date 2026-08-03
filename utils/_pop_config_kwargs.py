from typing import Any

def _pop_config_kwargs(config: dict[str, Any]) -> dict[str, Any]:
    """Extract triton.Config options that should become kwargs"""
    popped = {}
    for key in (
        "num_warps",
        "num_stages",
        "num_ctas",
        "maxnreg",
        "num_consumer_groups",
        "num_buffers_warp_spec",
    ):
        val = config.pop(key, None)
        if val is not None:
            popped[key] = val
    return popped

