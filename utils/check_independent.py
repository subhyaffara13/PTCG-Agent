
def check_independent(basis):
    if len(basis) == 0:
        return

    np = pytest.importorskip("numpy")
    sp = pytest.importorskip("scipy")  # Required by incidence_matrix

    H = nx.Graph()
    for b in basis:
        nx.add_cycle(H, b)
    inc = nx.incidence_matrix(H, oriented=True)
    rank = np.linalg.matrix_rank(inc.toarray(), tol=None, hermitian=False)
    assert inc.shape[1] - rank == len(basis)

