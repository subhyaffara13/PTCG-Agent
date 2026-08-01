
def test_symmetric_graph_laplacian():
    symmetric_mats = (
        'np.arange(10) * np.arange(10)[:, np.newaxis]',
        'np.ones((7, 7))',
        'np.eye(19)',
        'sparse.diags_array([1.0, 1.0], offsets=[-1, 1], shape=(4, 4))',
        'sparse.diags_array([1.0, 1.0], offsets=[-1, 1], shape=(4, 4)).toarray()',
        'sparse.diags_array([1.0, 1.0], offsets=[-1, 1], shape=(4, 4)).todense()',
        'np.vander(np.arange(4)) + np.vander(np.arange(4)).T'
    )
    for mat in symmetric_mats:
        for normed in True, False:
            for copy in True, False:
                _check_symmetric_graph_laplacian(mat, normed, copy)

