
def calculate_table_statistics(
    flat_table: list[dict[str, str]]
) -> dict[str, dict[str, int]]:
    """Get counts of what is supported per module.

    Parameters
    ----------
    flat_table : list[dict[str, str]]
        A table as returned by `make_flat_capabilities_table`

    Returns
    -------
    dict[str, dict[str, int]]
        dict mapping module names to inner dicts.
        bool. The inner dicts have a key "total" along with keys for each
        backend column of the supplied flat capabilities table. The value
        corresponding to total is the total count of functions in the given
        module, and the value associated to the other keys is the count of
        functions that support that particular backend.
    """
    if not flat_table:
        return {}

    counter: defaultdict[str, defaultdict[str, int]]
    counter = defaultdict(lambda: defaultdict(int))

    S = BackendSupportStatus
    for entry in flat_table:
        entry = entry.copy()
        entry.pop("function")
        module = entry.pop("module")
        current_counter = counter[module]

        # By design, all backends and options must be considered out-of-scope
        # if one is, so just pick an arbitrary entry here to test if function is
        # in-scope.
        if next(iter(entry.values())) != S.OUT_OF_SCOPE:
            current_counter["total"] += 1
            for key, value in entry.items():
                # Functions missing xp_capabilities will be tabulated as
                # unsupported, but may actually be supported. There is a
                # note about this in the documentation and this function is
                # set up to return information needed to put asterisks next
                # to percentages impacted by missing xp_capabilities decorators.
                current_counter[key] += 1 if value == S.YES else 0
    return {mod: dict(counts) for mod, counts in counter.items()}

