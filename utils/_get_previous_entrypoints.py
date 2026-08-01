
def _get_previous_entrypoints(dist: Distribution) -> dict[str, list]:
    ignore = ("console_scripts", "gui_scripts")
    value = getattr(dist, "entry_points", None) or {}
    return {k: v for k, v in value.items() if k not in ignore}

