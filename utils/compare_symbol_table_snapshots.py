
def compare_symbol_table_snapshots(
    name_prefix: str, snapshot1: dict[str, SymbolSnapshot], snapshot2: dict[str, SymbolSnapshot]
) -> set[str]:
    """Return names that are different in two snapshots of a symbol table.

    Only shallow (intra-module) differences are considered. References to things defined
    outside the module are compared based on the name of the target only.

    Recurse into class symbol tables (if the class is defined in the target module).

    Return a set of fully-qualified names (e.g., 'mod.func' or 'mod.Class.method').
    """
    # Find names only defined only in one version.
    names1 = {f"{name_prefix}.{name}" for name in snapshot1}
    names2 = {f"{name_prefix}.{name}" for name in snapshot2}
    triggers = names1 ^ names2

    # Look for names defined in both versions that are different.
    for name in set(snapshot1.keys()) & set(snapshot2.keys()):
        item1 = snapshot1[name]
        item2 = snapshot2[name]
        kind1 = item1[0]
        kind2 = item2[0]
        item_name = f"{name_prefix}.{name}"
        if kind1 != kind2:
            # Different kind of node in two snapshots -> trivially different.
            triggers.add(item_name)
        elif kind1 == "TypeInfo":
            if item1[:-1] != item2[:-1]:
                # Record major difference (outside class symbol tables).
                triggers.add(item_name)
            # Look for differences in nested class symbol table entries.
            assert isinstance(item1[-1], dict)
            assert isinstance(item2[-1], dict)
            triggers |= compare_symbol_table_snapshots(item_name, item1[-1], item2[-1])
        else:
            # Shallow node (no interesting internal structure). Just use equality.
            if snapshot1[name] != snapshot2[name]:
                triggers.add(item_name)

    return triggers

