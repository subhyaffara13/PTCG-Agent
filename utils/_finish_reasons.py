
def _finish_reasons(choices: tuple[Mapping[str, object], ...]) -> tuple[str, ...]:
    """Non-empty ``finish_reason`` of each response choice."""
    return tuple(r for c in choices if (r := as_str(c.get("finish_reason"))))

