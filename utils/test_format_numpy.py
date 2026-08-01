
def test_format_numpy():
    if not np:
        skip("numpy not installed.")

    for test in _tests:
        lhs = represent(test[0], basis=A, format='numpy')
        rhs = to_numpy(test[1])
        if isinstance(lhs, numpy_ndarray):
            assert (lhs == rhs).all()
        else:
            assert lhs == rhs

