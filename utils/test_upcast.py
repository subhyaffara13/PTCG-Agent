
def test_upcast():
    a0 = csr_matrix([[np.pi, np.pi*1j], [3, 4]], dtype=complex)
    b0 = np.array([256+1j, 2**32], dtype=complex)

    for a_dtype in supported_dtypes:
        for b_dtype in supported_dtypes:
            msg = f"({a_dtype!r}, {b_dtype!r})"

            if np.issubdtype(a_dtype, np.complexfloating):
                a = a0.copy().astype(a_dtype)
            else:
                a = a0.real.copy().astype(a_dtype)

            if np.issubdtype(b_dtype, np.complexfloating):
                b = b0.copy().astype(b_dtype)
            else:
                with np.errstate(invalid="ignore"):
                    # Casting a large value (2**32) to int8 causes a warning in
                    # numpy >1.23
                    b = b0.real.copy().astype(b_dtype)

            if not (a_dtype == np.bool_ and b_dtype == np.bool_):
                c = np.zeros((2,), dtype=np.bool_)
                assert_raises(ValueError, _sparsetools.csr_matvec,
                              2, 2, a.indptr, a.indices, a.data, b, c)

            if ((np.issubdtype(a_dtype, np.complexfloating) and
                 not np.issubdtype(b_dtype, np.complexfloating)) or
                (not np.issubdtype(a_dtype, np.complexfloating) and
                 np.issubdtype(b_dtype, np.complexfloating))):
                c = np.zeros((2,), dtype=np.float64)
                assert_raises(ValueError, _sparsetools.csr_matvec,
                              2, 2, a.indptr, a.indices, a.data, b, c)

            c = np.zeros((2,), dtype=np.result_type(a_dtype, b_dtype))
            _sparsetools.csr_matvec(2, 2, a.indptr, a.indices, a.data, b, c)
            assert_allclose(c, np.dot(a.toarray(), b), err_msg=msg)

