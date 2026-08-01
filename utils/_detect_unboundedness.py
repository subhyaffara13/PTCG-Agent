
def _detect_unboundedness(R):
    """Detect infinite-capacity negative cycles."""
    G = nx.DiGraph()
    G.add_nodes_from(R)

    # Value simulating infinity.
    inf = R.graph["inf"]
    # True infinity.
    f_inf = float("inf")
    for u in R:
        for v, e in R[u].items():
            # Compute the minimum weight of infinite-capacity (u, v) edges.
            w = f_inf
            for k, e in e.items():
                if e["capacity"] == inf:
                    w = min(w, e["weight"])
            if w != f_inf:
                G.add_edge(u, v, weight=w)

    if nx.negative_edge_cycle(G):
        raise nx.NetworkXUnbounded(
            "Negative cost cycle of infinite capacity found. "
            "Min cost flow may be unbounded below."
        )

