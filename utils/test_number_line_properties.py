
def test_number_line_properties():
    # From:
    # https://en.wikipedia.org/wiki/Inequality_(mathematics)#Properties_on_the_number_line

    a, b, c = symbols("a b c", real=True)

    # Transitivity
    # If a <= b and b <= c, then a <= c.
    assert ask(a <= c, (a <= b) & (b <= c)) is True
    # If a <= b and b < c, then a < c.
    assert ask(a < c, (a <= b) & (b < c)) is True
    # If a < b and b <= c, then a < c.
    assert ask(a < c, (a < b) & (b <= c)) is True

    # Addition and subtraction
    # If a <= b, then a + c <= b + c and a - c <= b - c.
    assert ask(a + c <= b + c, a <= b) is True
    assert ask(a - c <= b - c, a <= b) is True

