
def test_flatiter_method_signatures(methodname: str):
    method = getattr(np.flatiter, methodname)
    assert callable(method)

    try:
        sig = inspect.signature(method)
    except ValueError as e:
        pytest.fail(f"Could not get signature for np.flatiter.{methodname}: {e}")

    assert "self" in sig.parameters
    assert sig.parameters["self"].kind is inspect.Parameter.POSITIONAL_ONLY

