
def test_asymmetric_laplacian(use_out_degree, normed,
                              copy, dtype, arr_type):
    # adjacency matrix
    A = [[0, 1, 0],
         [4, 2, 0],
         [0, 0, 0]]
    A = arr_type(np.array(A), dtype=dtype)
    A_copy = A.copy()

    if not normed and use_out_degree:
        # Laplacian matrix using out-degree
        L = [[1, -1, 0],
             [-4, 4, 0],
             [0, 0, 0]]
        d = [1, 4, 0]

    if normed and use_out_degree:
        # normalized Laplacian matrix using out-degree
        L = [[1, -0.5, 0],
             [-2, 1, 0],
             [0, 0, 0]]
        d = [1, 2, 1]

    if not normed and not use_out_degree:
        # Laplacian matrix using in-degree
        L = [[4, -1, 0],
             [-4, 1, 0],
             [0, 0, 0]]
        d = [4, 1, 0]

    if normed and not use_out_degree:
        # normalized Laplacian matrix using in-degree
        L = [[1, -0.5, 0],
             [-2, 1, 0],
             [0, 0, 0]]
        d = [2, 1, 1]

    _check_laplacian_dtype_none(
        A,
        L,
        d,
        normed=normed,
        use_out_degree=use_out_degree,
        copy=copy,
        dtype=dtype,
        arr_type=arr_type,
    )

    _check_laplacian_dtype(
        A_copy,
        L,
        d,
        normed=normed,
        use_out_degree=use_out_degree,
        copy=copy,
        dtype=dtype,
        arr_type=arr_type,
    )

