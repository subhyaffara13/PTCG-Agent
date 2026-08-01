
def dedup_vars(vars: Sequence[SavedAttribute]) -> Sequence[SavedAttribute]:
    seen: set[str] = set()
    saved: list[SavedAttribute] = []
    for var in vars:
        name = (
            var.nctype.name.name
            if isinstance(var.nctype.name, SpecialArgName)
            else var.nctype.name
        )
        if name in seen:
            continue
        seen.add(name)
        saved.append(var)
    return saved

