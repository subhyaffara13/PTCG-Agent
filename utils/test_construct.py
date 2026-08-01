
def test_construct():
    expr     = Compound(Basic, (S(1), S(2), S(3)))
    expected = Basic(S(1), S(2), S(3))
    assert construct(expr) == expected


def test_construct() -> None:
    """Tests that we can construct UuidExtensionArray from a list of valid values."""
    from uuid import uuid4

    a = UuidExtensionArray([UUID(int=0), u := uuid4()])
    assert a[0].int == 0
    assert a[1] == u

