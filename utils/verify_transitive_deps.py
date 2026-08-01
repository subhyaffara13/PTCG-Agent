
def verify_transitive_deps(ascc: SCC, graph: Graph, manager: BuildManager) -> str | None:
    """Verify all indirect dependencies of this SCC are still reachable via direct ones.

    Return first unreachable dependency id, or None.
    """
    for id in ascc.mod_ids:
        st = graph[id]
        assert st.meta is not None, "Must be called on fresh SCCs only"
        if st.trans_dep_hash == st.meta.trans_dep_hash:
            # Import graph unchanged, skip this module.
            continue
        for dep in st.dependencies:
            if st.priorities.get(dep) == PRI_INDIRECT:
                dep_scc_id = manager.scc_by_mod_id[dep].id
                if dep_scc_id == ascc.id:
                    continue
                if not manager.is_transitive_scc_dep(ascc.id, dep_scc_id):
                    return dep
    return None

