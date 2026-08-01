
def test_P3():
    A = Matrix([
        [11, 12, 13, 14],
        [21, 22, 23, 24],
        [31, 32, 33, 34],
        [41, 42, 43, 44]])

    A11 = A[0:3, 1:4]
    A12 = A[(0, 1, 3), (2, 0, 3)]
    A21 = A
    A221 = -A[0:2, 2:4]
    A222 = -A[(3, 0), (2, 1)]
    A22 = BlockMatrix([[A221, A222]]).T
    rows = [[-A11, A12], [A21, A22]]
    raises(ValueError, lambda: BlockMatrix(rows))
    B = Matrix(rows)
    assert B == Matrix([
        [-12, -13, -14, 13, 11, 14],
        [-22, -23, -24, 23, 21, 24],
        [-32, -33, -34, 43, 41, 44],
        [11, 12, 13, 14, -13, -23],
        [21, 22, 23, 24, -14, -24],
        [31, 32, 33, 34, -43, -13],
        [41, 42, 43, 44, -42, -12]])


def test_P3():
    """Second order centrality: line graph, as defined in paper"""
    G = nx.path_graph(3)
    b_answer = {0: 3.741, 1: 1.414, 2: 3.741}

    b = nx.second_order_centrality(G)

    for n in sorted(G):
        assert b[n] == pytest.approx(b_answer[n], abs=1e-2)

