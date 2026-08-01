
def test_scalar_for_scalar(case):
    # Some rv_continuous functions returned 0d array instead of NumPy scalar
    # Guard against regression
    method_name, args = case
    method = getattr(stats.norm(), method_name)
    res = method(*args)
    if case in scalar_out:
        assert isinstance(res, np.number)
    else:
        assert isinstance(res[0], np.number)
        assert isinstance(res[1], np.number)

