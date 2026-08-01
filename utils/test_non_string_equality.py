
def test_non_string_equality():
    # Expressions should not compare equal to strings
    x = symbols('x')
    one = sympify(1)
    assert (x == 'x') is False
    assert (x != 'x') is True
    assert (one == '1') is False
    assert (one != '1') is True
    assert (x + 1 == 'x + 1') is False
    assert (x + 1 != 'x + 1') is True

    # Make sure == doesn't try to convert the resulting expression to a string
    # (e.g., by calling sympify() instead of _sympify())

    class BadRepr:
        def __repr__(self):
            raise RuntimeError

    assert (x == BadRepr()) is False
    assert (x != BadRepr()) is True

