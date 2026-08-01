
def _dict2graph(d):
    nodes = list(d)
    edges = [(f1, f2) for f1, f2s in d.items() for f2 in f2s]
    G = (nodes, edges)
    return G

