
def _memo_connectivity(G, u, v, memo):
    edge = (u, v)
    if edge in memo:
        return memo[edge]
    if not G.is_directed():
        redge = (v, u)
        if redge in memo:
            return memo[redge]
    memo[edge] = nx.edge_connectivity(G, *edge)
    return memo[edge]

