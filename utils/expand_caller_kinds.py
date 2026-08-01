
def expand_caller_kinds(
    kinds_or_names: list[ArgKind | str],
) -> tuple[list[ArgKind], list[str | None]]:
    kinds = []
    names: list[str | None] = []
    for k in kinds_or_names:
        if isinstance(k, str):
            kinds.append(ARG_NAMED)
            names.append(k)
        else:
            kinds.append(k)
            names.append(None)
    return kinds, names

