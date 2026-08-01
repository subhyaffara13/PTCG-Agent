
def graphs(sparse_cls):
    graph = [
        [0, 1, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0],
    ]
    A_dense = np.array(graph)
    A_sparse = sparse_cls(A_dense)
    return A_dense, A_sparse

