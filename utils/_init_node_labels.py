
def _init_node_labels(G, edge_attr, node_attr):
    if node_attr:
        return {u: str(dd[node_attr]) for u, dd in G.nodes(data=True)}
    elif edge_attr:
        return {u: "" for u in G}
    else:
        warnings.warn(
            "The hashes produced for graphs without node or edge attributes "
            "changed in v3.5 due to a bugfix (see documentation).",
            UserWarning,
            stacklevel=2,
        )
        if nx.is_directed(G):
            return {u: str(G.in_degree(u)) + "_" + str(G.out_degree(u)) for u in G}
        else:
            return {u: str(deg) for u, deg in G.degree()}

