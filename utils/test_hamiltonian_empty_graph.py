
def test_hamiltonian_empty_graph():
    path = hamiltonian_path(DiGraph())
    assert len(path) == 0

