
def test_index_dtype_compressed(cls, indices_attrs, expected_dtype):
    input_array = scipy.sparse.coo_array(np.arange(9).reshape(3, 3))
    coo_tuple = (
        input_array.data,
        (
            input_array.row.astype(expected_dtype),
            input_array.col.astype(expected_dtype),
        )
    )

    result = cls(coo_tuple)
    for attr in indices_attrs:
        assert getattr(result, attr).dtype == expected_dtype

    result = cls(coo_tuple, shape=(3, 3))
    for attr in indices_attrs:
        assert getattr(result, attr).dtype == expected_dtype

    if issubclass(cls, scipy.sparse._compressed._cs_matrix):
        input_array_csr = input_array.tocsr()
        csr_tuple = (
            input_array_csr.data,
            input_array_csr.indices.astype(expected_dtype),
            input_array_csr.indptr.astype(expected_dtype),
        )

        result = cls(csr_tuple)
        for attr in indices_attrs:
            assert getattr(result, attr).dtype == expected_dtype

        result = cls(csr_tuple, shape=(3, 3))
        for attr in indices_attrs:
            assert getattr(result, attr).dtype == expected_dtype

