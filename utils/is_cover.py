
def is_cover(G, node_cover):
    return all({u, v} & node_cover for u, v in G.edges())

