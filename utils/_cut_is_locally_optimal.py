
def _cut_is_locally_optimal(G, cut_size, set1):
    # test if cut can be locally improved
    for i, node in enumerate(set1):
        cut_size_without_node = nx.algorithms.cut_size(
            G, set1 - {node}, weight="weight"
        )
        assert cut_size_without_node <= cut_size

