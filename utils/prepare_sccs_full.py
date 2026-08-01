
def prepare_sccs_full(
    raw_sccs: Iterator[set[str]], edges: dict[str, list[str]]
) -> dict[SCC, set[SCC]]:
    """Turn raw SCC sets into SCC objects and build dependency graph for SCCs."""
    sccs = [SCC(raw_scc) for raw_scc in raw_sccs]
    scc_map = {}
    for scc in sccs:
        for id in scc.mod_ids:
            scc_map[id] = scc
    scc_deps_map: dict[SCC, set[SCC]] = {}
    for scc in sccs:
        for id in scc.mod_ids:
            scc_deps_map.setdefault(scc, set()).update(scc_map[dep] for dep in edges[id])
    for scc in sccs:
        # Remove trivial dependency on itself.
        scc_deps_map[scc].discard(scc)
        dep_sccs = scc_deps_map[scc]
        for dep_scc in dep_sccs:
            scc.deps.add(dep_scc.id)
        scc.not_ready_count = len(dep_sccs)
    return scc_deps_map

