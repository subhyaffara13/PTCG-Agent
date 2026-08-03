import copy

def test_sparse_formats(fmt, normed, copy):
    mat = sparse.diags_array([1.0, 1.0], offsets=[-1, 1], shape=(4, 4), format=fmt)
    _check_symmetric_graph_laplacian(mat, normed, copy)

