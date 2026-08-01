
def test_is_numeric(idx):
    # MultiIndex is never numeric
    assert not is_any_real_numeric_dtype(idx)


def test_is_numeric(dtype, expected):
    dtype = NumpyEADtype(dtype)
    assert dtype._is_numeric is expected


def test_is_numeric(dtype, expected):
    assert SparseDtype(dtype)._is_numeric is expected


def test_is_numeric():
    assert SF._is_numeric

