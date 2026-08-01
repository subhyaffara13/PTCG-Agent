
def order_ascc_ex(graph: Graph, ascc: SCC) -> list[str]:
    """Apply extra heuristics on top of order_ascc().

    This should be used only for actual SCCs, not for "inner" SCCs
    we create recursively during ordering of the SCC. Currently, this
    has only some special handling for builtin SCC.
    """
    scc = order_ascc(graph, ascc.mod_ids)
    # Make the order of the SCC that includes 'builtins' and 'typing',
    # among other things, predictable. Various things may  break if
    # the order changes.
    if "builtins" in ascc.mod_ids:
        scc = sorted(scc, reverse=True)
        # If builtins is in the list, move it last.  (This is a bit of
        # a hack, but it's necessary because the builtins module is
        # part of a small cycle involving at least {builtins, abc,
        # typing}.  Of these, builtins must be processed last or else
        # some builtin objects will be incompletely processed.)
        scc.remove("builtins")
        scc.append("builtins")
    return scc

