
def test_strongly_connected_components():
    assert strongly_connected_components(([], [])) == []
    assert strongly_connected_components(([1, 2, 3], [])) == [[1], [2], [3]]

    V = [1, 2, 3]
    E = [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1)]
    assert strongly_connected_components((V, E)) == [[1, 2, 3]]

    V = [1, 2, 3, 4]
    E = [(1, 2), (2, 3), (3, 2), (3, 4)]
    assert strongly_connected_components((V, E)) == [[4], [2, 3], [1]]

    V = [1, 2, 3, 4]
    E = [(1, 2), (2, 1), (3, 4), (4, 3)]
    assert strongly_connected_components((V, E)) == [[1, 2], [3, 4]]


def test_strongly_connected_components():
    M = Matrix([
        [11, 14, 10, 0, 15, 0],
        [0, 44, 0, 0, 45, 0],
        [1, 4, 0, 0, 5, 0],
        [0, 0, 0, 22, 0, 23],
        [0, 54, 0, 0, 55, 0],
        [0, 0, 0, 32, 0, 33]])
    scc = M.strongly_connected_components()
    assert scc == [[1, 4], [0, 2], [3, 5]]

    P, B = M.strongly_connected_components_decomposition()
    p = Permutation([1, 4, 0, 2, 3, 5])
    assert P == PermutationMatrix(p)
    assert B == BlockMatrix([
        [
            Matrix([[44, 45], [54, 55]]),
            Matrix.zeros(2, 2),
            Matrix.zeros(2, 2)
        ],
        [
            Matrix([[14, 15], [4, 5]]),
            Matrix([[11, 10], [1, 0]]),
            Matrix.zeros(2, 2)
        ],
        [
            Matrix.zeros(2, 2),
            Matrix.zeros(2, 2),
            Matrix([[22, 23], [32, 33]])
        ]
    ])
    P = P.as_explicit()
    B = B.as_explicit()
    assert P.T * B * P == M

    P, B = M.strongly_connected_components_decomposition(lower=False)
    p = Permutation([3, 5, 0, 2, 1, 4])
    assert P == PermutationMatrix(p)
    assert B == BlockMatrix([
        [
            Matrix([[22, 23], [32, 33]]),
            Matrix.zeros(2, 2),
            Matrix.zeros(2, 2)
        ],
        [
            Matrix.zeros(2, 2),
            Matrix([[11, 10], [1, 0]]),
            Matrix([[14, 15], [4, 5]])
        ],
        [
            Matrix.zeros(2, 2),
            Matrix.zeros(2, 2),
            Matrix([[44, 45], [54, 55]])
        ]
    ])
    P = P.as_explicit()
    B = B.as_explicit()
    assert P.T * B * P == M

