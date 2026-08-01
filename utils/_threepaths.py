
def _threepaths(G):
    paths = 0
    for v in G:
        for u in G[v]:
            for w in set(G[u]) - {v}:
                paths += len(set(G[w]) - {v, u})
    # Divide by two because we count each three path twice
    # one for each possible starting point
    return paths / 2

