
def expand_callee_kinds(
    kinds_and_names: list[ArgKind | tuple[ArgKind, str]],
) -> tuple[list[ArgKind], list[str | None]]:
    kinds = []
    names: list[str | None] = []
    for v in kinds_and_names:
        if isinstance(v, tuple):
            kinds.append(v[0])
            names.append(v[1])
        else:
            kinds.append(v)
            names.append(None)
    return kinds, names

