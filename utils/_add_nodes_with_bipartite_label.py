
def _add_nodes_with_bipartite_label(G, lena, lenb):
    G.add_nodes_from(range(lena + lenb))
    b = dict(zip(range(lena), [0] * lena))
    b.update(dict(zip(range(lena, lena + lenb), [1] * lenb)))
    nx.set_node_attributes(G, b, "bipartite")
    return G

