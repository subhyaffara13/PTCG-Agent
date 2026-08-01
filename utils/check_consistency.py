
def check_consistency(o: object) -> None:
    """Fail if there are two AST nodes with the same fullname reachable from 'o'.

    Raise AssertionError on failure and print some debugging output.
    """
    seen, parents = get_reachable_graph(o)
    reachable = list(seen.values())
    syms = [x for x in reachable if isinstance(x, SymbolNode)]

    m: dict[str, SymbolNode] = {}
    for sym in syms:
        if isinstance(sym, FakeInfo):
            continue

        fn = sym.fullname
        # Skip None and empty names, since they are ambiguous.
        # TODO: Everything should have a proper full name?
        if not fn:
            continue

        # Skip stuff that should be expected to have duplicate names
        if isinstance(sym, (Var, Decorator)):
            continue
        if isinstance(sym, FuncDef) and sym.is_overload:
            continue

        if fn not in m:
            m[fn] = sym
            continue

        # We have trouble and need to decide what to do about it.
        sym1, sym2 = sym, m[fn]

        # If the type changed, then it shouldn't have been merged.
        if type(sym1) is not type(sym2):
            continue

        path1 = get_path(sym1, seen, parents)
        path2 = get_path(sym2, seen, parents)

        if fn in m:
            print(f"\nDuplicate {type(sym).__name__!r} nodes with fullname {fn!r} found:")
            print("[1] %d: %s" % (id(sym1), path_to_str(path1)))
            print("[2] %d: %s" % (id(sym2), path_to_str(path2)))

        if DUMP_MISMATCH_NODES and fn in m:
            # Add verbose output with full AST node contents.
            print("---")
            print(id(sym1), sym1)
            print("---")
            print(id(sym2), sym2)

        assert sym.fullname not in m

