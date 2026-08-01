
def test_maybe_mangle_lambdas_named():
    func = {"C": np.mean, "D": {"foo": np.mean, "bar": np.mean}}
    result = maybe_mangle_lambdas(func)
    assert result == func

