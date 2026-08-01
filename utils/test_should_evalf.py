
def test_should_evalf():
    # This should not take forever to run (see #8506)
    assert isinstance(sin((1.0 + 1.0*I)**10000 + 1), sin)

