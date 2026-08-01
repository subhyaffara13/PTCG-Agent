
def test_user_defined_floating_dtype_printing_does_not_corrupt_precision():
    """
    Ensure that array printing does not use NumPy Dragon4 formatting
    for user-defined floating dtypes, which would silently truncate
    precision to float64.
    """
    # Quaddtype (<=1.0.0) may have a bug that leads to test failures elsewhere
    # (this may also be an interplay of numpy/quaddtype but let's hope new
    # quaddtype versions will fix it.)
    from importlib.metadata import version

    try:
        quaddtype_version = version("numpy_quaddtype")
    except Exception:
        pytest.skip("numpy_quaddtype not installed")
    else:
        if _pep440.Version(quaddtype_version) <= _pep440.Version("1.0.0"):
            pytest.skip("critical bug in quaddtype during import")

    numpy_quaddtype = pytest.importorskip("numpy_quaddtype")

    pi_str = "3.14159265358979323846264338327950288"
    arr = np.array([pi_str], dtype=QuadPrecDType())
    res = np.array(str(arr).strip("[] "), dtype=QuadPrecDType())
    # Check that the string representation round-trips correctly.
    assert_array_equal(res, arr)

