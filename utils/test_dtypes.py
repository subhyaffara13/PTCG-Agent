
def test_dtypes():
    # See issue #1328.
    # - Platform-dependent sizes.
    for size_check in m.get_platform_dtype_size_checks():
        print(size_check)
        assert size_check.size_cpp == size_check.size_numpy, size_check
    # - Concrete sizes.
    for check in m.get_concrete_dtype_checks():
        print(check)
        assert check.numpy == check.pybind11, check
        if check.numpy.num != check.pybind11.num:
            print(
                f"NOTE: typenum mismatch for {check}: {check.numpy.num} != {check.pybind11.num}"
            )


def test_dtypes(vdtype, mdtype, arr_type):
    """Test lobpcg in various dtypes.
    """
    rnd = np.random.RandomState(0)
    n = 12
    m = 2
    A = arr_type(np.diag(np.arange(1, n + 1)).astype(mdtype))
    X = rnd.random((n, m))
    X = X.astype(vdtype)
    eigvals, eigvecs = lobpcg(A, X, tol=1e-2, largest=False)
    assert_allclose(eigvals, np.arange(1, 1 + m), atol=1e-1)
    # eigenvectors must be nearly real in any case
    assert_allclose(np.sum(np.abs(eigvecs - eigvecs.conj())), 0, atol=1e-2)


def test_dtypes(dtype):
    # smoke tests on auto dtype construction

    np.dtype(dtype.type).kind == "f"
    assert dtype.name is not None


def test_dtypes(dtype):
    # smoke tests on auto dtype construction

    if dtype.is_signed_integer:
        assert np.dtype(dtype.type).kind == "i"
    else:
        assert np.dtype(dtype.type).kind == "u"
    assert dtype.name is not None


def test_dtypes(dtype):
    # smoke tests on auto dtype construction

    if dtype.is_signed_integer:
        assert np.dtype(dtype.type).kind == "i"
    else:
        assert np.dtype(dtype.type).kind == "u"
    assert dtype.name is not None

