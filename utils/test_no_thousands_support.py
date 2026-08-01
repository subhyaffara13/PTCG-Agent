
def test_no_thousands_support(dtype):
    # Mainly to document behaviour, Python supports thousands like 1_1.
    # (e and G may end up using different conversion and support it, this is
    # a bug but happens...)
    if dtype == "e":
        pytest.skip("half assignment currently uses Python float converter")
    if dtype in "eG":
        pytest.xfail("clongdouble assignment is buggy (uses `complex`?).")

    assert int("1_1") == float("1_1") == complex("1_1") == 11
    with pytest.raises(ValueError):
        np.loadtxt(["1_1\n"], dtype=dtype)

