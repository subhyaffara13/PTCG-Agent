
def pseudo_peripheral_node(G):
    # helper for cuthill-mckee to find a node in a "pseudo peripheral pair"
    # to use as good starting node
    u = arbitrary_element(G)
    lp = 0
    v = u
    while True:
        spl = nx.shortest_path_length(G, v)
        l = max(spl.values())
        if l <= lp:
            break
        lp = l
        farthest = (n for n, dist in spl.items() if dist == l)
        v, deg = min(G.degree(farthest), key=itemgetter(1))
    return v

