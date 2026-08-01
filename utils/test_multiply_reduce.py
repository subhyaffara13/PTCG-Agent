
def test_multiply_reduce():
    # At the time of writing (NumPy 2.0) this is very limited (and rather
    # ridiculous anyway).  But it works and actually makes some sense...
    # (NumPy does not allow non-scalar initial values)
    repeats = np.array([2, 3, 4])
    val = "school-🚌"
    res = np.multiply.reduce(repeats, initial=val, dtype=np.dtypes.StringDType)
    assert res == val * np.prod(repeats)

