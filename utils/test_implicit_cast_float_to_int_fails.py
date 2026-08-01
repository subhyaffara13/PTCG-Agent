
def test_implicit_cast_float_to_int_fails(dtype):
    txt = StringIO("1.0, 2.1, 3.7\n4, 5, 6")
    with pytest.raises(ValueError):
        np.loadtxt(txt, dtype=dtype, delimiter=",")

