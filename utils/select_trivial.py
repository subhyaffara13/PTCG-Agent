
def select_trivial(options: Sequence[list[Constraint] | None]) -> list[list[Constraint]]:
    """Select only those lists where each item is a constraint against Any."""
    res = []
    for option in options:
        if option is None:
            continue
        if all(isinstance(get_proper_type(c.target), AnyType) for c in option):
            res.append(option)
    return res

