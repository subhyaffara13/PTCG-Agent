
def match_module_order(actual: list[str], expected_order: list[str]) -> list[str]:
    actual_by_mod = defaultdict(list)
    actual_order = module_order(actual)
    if set(actual_order) != set(expected_order):
        # Different files, give up and show actual errors.
        return actual
    for a in actual:
        mod, _ = a.split(":", maxsplit=1)
        actual_by_mod[mod].append(a)
    result = []
    for mod in expected_order:
        result.extend(actual_by_mod[mod])
    return result

