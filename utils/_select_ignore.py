
def _select_ignore(
    *,
    option: list[str] | None,
    default: tuple[str, ...],
    extended_default: list[str],
    extend: list[str] | None,
) -> tuple[str, ...]:
    # option was explicitly set, ignore the default and extended default
    if option is not None:
        ret = [*option, *(extend or [])]
    else:
        ret = [*default, *extended_default, *(extend or [])]
    return tuple(sorted(ret, reverse=True))

