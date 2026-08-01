
def test_failing_number_line_properties():
    # From:
    # https://en.wikipedia.org/wiki/Inequality_(mathematics)#Properties_on_the_number_line

    a, b, c = symbols("a b c", real=True)

    # Multiplication and division
    # If a <= b and c > 0, then ac <= bc and a/c <= b/c. (True for non-zero c)
    assert ask(a*c <= b*c, (a <= b) & (c > 0) & ~ Q.zero(c)) is True
    assert ask(a/c <= b/c, (a <= b) & (c > 0) & ~ Q.zero(c)) is True
    # If a <= b and c < 0, then ac >= bc and a/c >= b/c. (True for non-zero c)
    assert ask(a*c >= b*c, (a <= b) & (c < 0) & ~ Q.zero(c)) is True
    assert ask(a/c >= b/c, (a <= b) & (c < 0) & ~ Q.zero(c)) is True

    # Additive inverse
    # If a <= b, then -a >= -b.
    assert ask(-a >= -b, a <= b) is True

    # Multiplicative inverse
    # For a, b that are both negative or both positive:
    # If a <= b, then 1/a >= 1/b .
    assert ask(1/a >= 1/b, (a <= b) & Q.positive(x) & Q.positive(b)) is True
    assert ask(1/a >= 1/b, (a <= b) & Q.negative(x) & Q.negative(b)) is True

