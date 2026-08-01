
def transitive_dep_hash(scc: SCC, graph: Graph) -> bytes:
    """Compute stable snapshot of transitive import structure for given SCC."""
    mod_ids = scc.mod_ids
    if len(mod_ids) == 1:
        # Fast path: State.dependencies is already deduped and never contains
        # self.id, so we can skip the dedupe set and the self-membership check.
        (only_id,) = mod_ids
        st = graph[only_id]
        priorities = st.priorities
        all_direct_deps = sorted(
            dep for dep in st.dependencies if priorities.get(dep) != PRI_INDIRECT
        )
        buf = WriteBuffer()
        for dep_id in all_direct_deps:
            write_str_bare(buf, dep_id)
            write_bytes_bare(buf, graph[dep_id].trans_dep_hash)
        return hash_digest_bytes(buf.getvalue())
    deps_set: set[str] = set()
    for id in mod_ids:
        state = graph[id]
        priorities = state.priorities
        for dep in state.dependencies:
            if priorities.get(dep) != PRI_INDIRECT:
                deps_set.add(dep)
    all_direct_deps = sorted(deps_set)
    buf = WriteBuffer()
    for dep_id in all_direct_deps:
        write_str_bare(buf, dep_id)
        if dep_id not in mod_ids:
            write_bytes_bare(buf, graph[dep_id].trans_dep_hash)
    return hash_digest_bytes(buf.getvalue())

