
def test_hamiltonian_path():
    from itertools import permutations

    G = nx.complete_graph(4)
    paths = [list(p) for p in hamiltonian_path(G, 0)]
    exact = [[0] + list(p) for p in permutations([1, 2, 3], 3)]
    assert sorted(paths) == sorted(exact)

