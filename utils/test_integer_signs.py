
def test_integer_signs(dtype):
    dtype = np.dtype(dtype)
    assert np.loadtxt(["+2"], dtype=dtype) == 2
    if dtype.kind == "u":
        with pytest.raises(ValueError):
            np.loadtxt(["-1\n"], dtype=dtype)
    else:
        assert np.loadtxt(["-2\n"], dtype=dtype) == -2

    for sign in ["++", "+-", "--", "-+"]:
        with pytest.raises(ValueError):
            np.loadtxt([f"{sign}2\n"], dtype=dtype)

