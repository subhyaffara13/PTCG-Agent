
def test_reentrant_implicit_conversion_failure(msg):
    # ensure that there is no runaway reentrant implicit conversion (#1035)
    with pytest.raises(TypeError) as excinfo:
        m.BogusImplicitConversion(0)
    assert (
        msg(excinfo.value)
        == """
        __init__(): incompatible constructor arguments. The following argument types are supported:
            1. m.class_.BogusImplicitConversion(arg0: m.class_.BogusImplicitConversion)

        Invoked with: 0
    """
    )

