
def same_matrix(sparse_cls, sp_sparse_cls):
    np.random.seed(1234)
    A_dense = np.random.rand(9, 9)
    return sp_sparse_cls(A_dense), sparse_cls(A_dense)

