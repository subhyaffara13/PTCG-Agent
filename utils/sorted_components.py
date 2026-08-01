
def sorted_components(graph: Graph) -> list[SCC]:
    """Return the graph's SCCs, topologically sorted by dependencies.

    The sort order is from leaves (nodes without dependencies) to
    roots (nodes on which no other nodes depend).
    """
    # Compute SCCs.
    vertices = set(graph)
    edges = {id: deps_filtered(graph, vertices, id, PRI_INDIRECT) for id in vertices}
    scc_dep_map = prepare_sccs_full(strongly_connected_components(vertices, edges), edges)
    # Topsort.
    res = []
    for ready in topsort(scc_dep_map):
        # Sort the sets in ready by reversed smallest State.order.  Examples:
        #
        # - If ready is [{x}, {y}], x.order == 1, y.order == 2, we get
        #   [{y}, {x}].
        #
        # - If ready is [{a, b}, {c, d}], a.order == 1, b.order == 3,
        #   c.order == 2, d.order == 4, the sort keys become [1, 2]
        #   and the result is [{c, d}, {a, b}].
        sorted_ready = sorted(ready, key=lambda scc: -min(graph[id].order for id in scc.mod_ids))
        for scc in sorted_ready:
            scc.size_hint = sum(graph[mid].size_hint for mid in scc.mod_ids)
            for dep in scc_dep_map[scc]:
                dep.direct_dependents.append(scc.id)
            # We compute dependencies hash here since we know no direct
            # dependencies will be added or suppressed after this point.
            trans_dep_hash = transitive_dep_hash(scc, graph)
            for id in scc.mod_ids:
                graph[id].trans_dep_hash = trans_dep_hash
        res.extend(sorted_ready)
    return res

