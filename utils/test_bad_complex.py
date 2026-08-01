
def test_bad_complex(dtype, field):
    with pytest.raises(ValueError):
        np.loadtxt([field + "\n"], dtype=dtype, delimiter=",")

