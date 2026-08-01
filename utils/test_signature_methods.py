
def test_signature_methods(method):
    sig = inspect.signature(method)

    assert "self" in sig.parameters
    assert sig.parameters["self"].kind is inspect.Parameter.POSITIONAL_ONLY

