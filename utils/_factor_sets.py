
def _factor_sets(eqs: list[list]) -> set[frozenset]:
    """
    Helper that builds factor combinations.
    """
    if not eqs:
        return {frozenset()}

    current_set = min(eqs, key=len)
    other_sets = [s for s in eqs if s is not current_set]

    stack = [(factor, [s for s in other_sets if factor not in s], {factor})
             for factor in current_set]

    result = set()

    while stack:
        factor, remaining_sets, current_solution = stack.pop()

        if not remaining_sets:
            result.add(frozenset(current_solution))
            continue

        next_set = min(remaining_sets, key=len)
        next_remaining = [s for s in remaining_sets if s is not next_set]

        for next_factor in next_set:
            valid_remaining = [s for s in next_remaining if next_factor not in s]
            new_solution = current_solution | {next_factor}
            stack.append((next_factor, valid_remaining, new_solution))

    return {s1 for s1 in result if not any(s1 > s2 for s2 in result)}

