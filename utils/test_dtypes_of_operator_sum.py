
def test_dtypes_of_operator_sum(xp):
    # gh-6078

    mat_complex = xp.asarray(np.random.rand(2,2) + 1j * np.random.rand(2,2))
    mat_real = xp.asarray(np.random.rand(2,2))

    complex_operator = interface.aslinearoperator(mat_complex)
    real_operator = interface.aslinearoperator(mat_real)

    sum_complex = complex_operator + complex_operator
    sum_real = real_operator + real_operator

    assert sum_real.dtype == xp.float64
    assert sum_complex.dtype == xp.complex128

