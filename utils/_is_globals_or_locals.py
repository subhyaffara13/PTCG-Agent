
def _is_globals_or_locals(obj: typing.Any) -> bool:
    # These comparisons only make sense within this frame; still cheap to check.
    return obj is globals() or obj is locals()

