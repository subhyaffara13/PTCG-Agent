import random

def test_negative_weights(method):
    SP = shortest_path(directed_negative_weighted_G, method, directed=True)
    assert_allclose(SP, directed_negative_weighted_SP, atol=1e-10)


def test_negative_weights():
    G = nx.complete_graph(5)
    random.seed(5)
    for u, v, w in G.edges(data=True):
        w["weight"] = -1 * random.random()

    initial_cut = set(random.sample(sorted(G.nodes()), k=5))
    cut_size, (set1, set2) = maxcut.one_exchange(G, initial_cut, weight="weight")

    # make sure it is a valid cut
    _is_valid_cut(G, set1, set2)
    # check local optimality
    _cut_is_locally_optimal(G, cut_size, set1)
    # test that all nodes are in the same partition
    assert len(set1) == len(G.nodes) or len(set2) == len(G.nodes)

