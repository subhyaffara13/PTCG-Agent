
def is_coloring(G, coloring):
    """Determine if the coloring is a valid coloring for the graph G."""
    # Verify that the coloring is valid.
    return all(coloring[s] != coloring[d] for s, d in G.edges)

