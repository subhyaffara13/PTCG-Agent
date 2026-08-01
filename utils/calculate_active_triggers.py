
def calculate_active_triggers(
    manager: BuildManager,
    old_snapshots: dict[str, dict[str, SymbolSnapshot]],
    new_modules: dict[str, MypyFile | None],
) -> set[str]:
    """Determine activated triggers by comparing old and new symbol tables.

    For example, if only the signature of function m.f is different in the new
    symbol table, return {'<m.f>'}.
    """
    names: set[str] = set()
    for id in new_modules:
        snapshot1 = old_snapshots.get(id)
        if snapshot1 is None:
            names.add(id)
            snapshot1 = {}
        new = new_modules[id]
        if new is None:
            snapshot2 = snapshot_symbol_table(id, SymbolTable())
            names.add(id)
        else:
            snapshot2 = snapshot_symbol_table(id, new.names)
        diff = compare_symbol_table_snapshots(id, snapshot1, snapshot2)
        diff |= wildcard_triggers_for_changes(id, diff)
        names |= diff
    return {make_trigger(name) for name in names}

