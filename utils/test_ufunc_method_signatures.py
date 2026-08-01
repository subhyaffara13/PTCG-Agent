
def test_ufunc_method_signatures(methodname: str):
    method = getattr(np.ufunc, methodname)

    try:
        _ = inspect.signature(method)
    except ValueError as e:
        pytest.fail(e.args[0])

