
def _compute_placeholders(outer: Iterable[None | int | SymInt]) -> list[bool]:
    return [_is_symint_placeholder(s) for s in outer]

