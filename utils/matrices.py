
def matrices(sparse_cls):
    np.random.seed(1234)
    A_dense = np.random.rand(9, 9)
    A_dense = A_dense @ A_dense.T
    A_sparse = sparse_cls(A_dense)
    b = np.random.rand(9)
    return A_dense, A_sparse, b

