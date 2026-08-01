
def test_signature_constructor():
    sig = inspect.signature(np.nditer)

    assert sig.parameters
    assert "self" not in sig.parameters
    assert "args" not in sig.parameters
    assert "kwargs" not in sig.parameters

