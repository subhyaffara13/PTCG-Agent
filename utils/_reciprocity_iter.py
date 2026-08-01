
def _reciprocity_iter(G, nodes):
    """Return an iterator of (node, reciprocity)."""
    n = G.nbunch_iter(nodes)
    for node in n:
        pred = set(G.predecessors(node))
        succ = set(G.successors(node))
        overlap = pred & succ
        n_total = len(pred) + len(succ)

        # Reciprocity is not defined for isolated nodes.
        # Return None.
        if n_total == 0:
            yield (node, None)
        else:
            reciprocity = 2 * len(overlap) / n_total
            yield (node, reciprocity)

