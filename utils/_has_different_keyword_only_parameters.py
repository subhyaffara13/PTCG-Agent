
def _has_different_keyword_only_parameters(
    original: list[nodes.AssignName],
    overridden: list[nodes.AssignName],
) -> list[str]:
    """Determine if the two methods have different keyword only parameters."""
    original_names = [i.name for i in original]
    overridden_names = [i.name for i in overridden]

    if any(name not in overridden_names for name in original_names):
        return ["Number of parameters "]

    for name in overridden_names:
        if name in original_names:
            continue

        try:
            overridden[0].parent.default_value(name)
        except astroid.NoDefault:
            return ["Number of parameters "]

    return []

