
def gen_pyramid(N):
    # This graph admits a flow of value 1 for which every arc is at
    # capacity (except the arcs incident to the sink which have
    # infinite capacity).
    G = nx.DiGraph()

    for i in range(N - 1):
        cap = 1.0 / (i + 2)
        for j in range(i + 1):
            G.add_edge((i, j), (i + 1, j), capacity=cap)
            cap = 1.0 / (i + 1) - cap
            G.add_edge((i, j), (i + 1, j + 1), capacity=cap)
            cap = 1.0 / (i + 2) - cap

    for j in range(N):
        G.add_edge((N - 1, j), "t")

    return G

