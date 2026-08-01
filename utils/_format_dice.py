
def _format_dice(dice: Sequence[Mapping[str, Any]]) -> str:
    """Render the dice as ``"3, 5"`` (omit dice already consumed)."""
    if not dice:
        return "(none rolled)"
    remaining = [str(d.get("value")) for d in dice if not d.get("used")]
    if not remaining:
        return "(both dice already used)"
    return ", ".join(remaining)

