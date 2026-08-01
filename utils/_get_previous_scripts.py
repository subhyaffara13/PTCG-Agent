
def _get_previous_scripts(dist: Distribution) -> list | None:
    value = getattr(dist, "entry_points", None) or {}
    return value.get("console_scripts")

