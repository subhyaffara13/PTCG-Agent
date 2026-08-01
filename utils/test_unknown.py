
def test_unknown():
    """Check treatment of unknown objects.
    Objects without adjoint or conjugate/transpose methods
    are sympified and wrapped in dagger.
    """
    x = symbols("x", commutative=False)
    result = Dagger(x)
    assert result.args == (x,) and isinstance(result, adjoint)

