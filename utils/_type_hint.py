
def _type_hint(param) -> str:
    """Value hint for an option: enum choices inline as ``[a|b|c]``, otherwise the TYPE name.

    e.g. `--sort [downloads|likes|trending_score]` instead of `--sort CHOICE`.
    """
    choices = getattr(param.type, "choices", None)
    if choices:
        return "[" + "|".join(str(c) for c in choices) + "]"
    return getattr(param.type, "name", "").upper() or "VALUE"

