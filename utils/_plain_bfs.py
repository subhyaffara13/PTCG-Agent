
def _plain_bfs(G, n, source):
    """A fast BFS node generator"""
    adj = G._adj
    seen = {source}
    nextlevel = [source]
    while nextlevel:
        thislevel = nextlevel
        nextlevel = []
        for v in thislevel:
            for w in adj[v]:
                if w not in seen:
                    seen.add(w)
                    nextlevel.append(w)
            if len(seen) == n:
                return seen
    return seen


def _plain_bfs(G, n, source):
    """A fast BFS node generator

    The direction of the edge between nodes is ignored.

    For directed graphs only.

    """
    Gsucc = G._succ
    Gpred = G._pred
    seen = {source}
    nextlevel = [source]

    while nextlevel:
        thislevel = nextlevel
        nextlevel = []
        for v in thislevel:
            for w in Gsucc[v]:
                if w not in seen:
                    seen.add(w)
                    nextlevel.append(w)
            for w in Gpred[v]:
                if w not in seen:
                    seen.add(w)
                    nextlevel.append(w)
            if len(seen) == n:
                return seen
    return seen

