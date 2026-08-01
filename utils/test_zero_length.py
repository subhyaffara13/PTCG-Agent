
def test_zero_length(func, sizes):
    """Ignore strides on a length-0 dimension (even if they would be incompatible length > 1)"""
    assert np.all(func(np.zeros(sizes)) == np.zeros(sizes))


def test_zero_length():
    G = nx.cycle_graph(3)
    num_walks = nx.number_of_walks(G, 0)
    expected = {0: {0: 1, 1: 0, 2: 0}, 1: {0: 0, 1: 1, 2: 0}, 2: {0: 0, 1: 0, 2: 1}}
    assert num_walks == expected

