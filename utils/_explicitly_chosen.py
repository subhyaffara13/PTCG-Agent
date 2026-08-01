
def _explicitly_chosen(
    *,
    option: list[str] | None,
    extend: list[str] | None,
) -> tuple[str, ...]:
    ret = [*(option or []), *(extend or [])]
    return tuple(sorted(ret, reverse=True))

