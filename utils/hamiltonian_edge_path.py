
def hamiltonian_edge_path(G, source):
    source = arbitrary_element(G)
    neighbors = set(G[source]) - {source}
    n = len(G)
    for target in neighbors:
        for path in nx.all_simple_edge_paths(G, source, target):
            if len(path) == n - 1:
                yield path

