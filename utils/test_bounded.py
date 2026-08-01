
def test_bounded():
    assert limit(sin(x)/x, x, oo) == 0  # 216b
    assert limit(x*sin(1/x), x, 0) == 0  # 227a


def test_bounded():
    x, y, z = symbols('x,y,z')
    a = x + y
    x, y = a.args
    assert ask(Q.finite(a), Q.positive_infinite(y)) is None
    assert ask(Q.finite(x)) is None
    assert ask(Q.finite(x), Q.finite(x)) is True
    assert ask(Q.finite(x), Q.finite(y)) is None
    assert ask(Q.finite(x), Q.complex(x)) is True
    assert ask(Q.finite(x), Q.extended_real(x)) is None

    assert ask(Q.finite(x + 1)) is None
    assert ask(Q.finite(x + 1), Q.finite(x)) is True
    a = x + y
    x, y = a.args
    # B + B
    assert ask(Q.finite(a), Q.finite(x) & Q.finite(y)) is True
    assert ask(Q.finite(a), Q.positive(x) & Q.finite(y)) is True
    assert ask(Q.finite(a), Q.finite(x) & Q.positive(y)) is True
    assert ask(Q.finite(a), Q.positive(x) & Q.positive(y)) is True
    assert ask(Q.finite(a), Q.positive(x) & Q.finite(y)
        & ~Q.positive(y)) is True
    assert ask(Q.finite(a), Q.finite(x) & ~Q.positive(x)
        & Q.positive(y)) is True
    assert ask(Q.finite(a), Q.finite(x) & Q.finite(y) & ~Q.positive(x)
        & ~Q.positive(y)) is True
    # B + U
    assert ask(Q.finite(a), Q.finite(x) & ~Q.finite(y)) is False
    assert ask(Q.finite(a), Q.positive(x) & ~Q.finite(y)) is False
    assert ask(Q.finite(a), Q.finite(x)
        & Q.positive_infinite(y)) is False
    assert ask(Q.finite(a), Q.positive(x)
        & Q.positive_infinite(y)) is False
    assert ask(Q.finite(a), Q.positive(x) & ~Q.finite(y)
        & ~Q.positive(y)) is False
    assert ask(Q.finite(a), Q.finite(x) & ~Q.positive(x)
        & Q.positive_infinite(y)) is False
    assert ask(Q.finite(a), Q.finite(x) & ~Q.positive(x) & ~Q.finite(y)
        & ~Q.positive(y)) is False
    # B + ?
    assert ask(Q.finite(a), Q.finite(x)) is None
    assert ask(Q.finite(a), Q.positive(x)) is None
    assert ask(Q.finite(a), Q.finite(x)
        & Q.extended_positive(y)) is None
    assert ask(Q.finite(a), Q.positive(x)
        & Q.extended_positive(y)) is None
    assert ask(Q.finite(a), Q.positive(x) & ~Q.positive(y)) is None
    assert ask(Q.finite(a), Q.finite(x) & ~Q.positive(x)
        & Q.extended_positive(y)) is None
    assert ask(Q.finite(a), Q.finite(x) & ~Q.positive(x)
        & ~Q.positive(y)) is None
    # U + U
    assert ask(Q.finite(a), ~Q.finite(x) & ~Q.finite(y)) is None
    assert ask(Q.finite(a), Q.positive_infinite(x)
        & ~Q.finite(y)) is None
    assert ask(Q.finite(a), ~Q.finite(x)
        & Q.positive_infinite(y)) is None
    assert ask(Q.finite(a), Q.positive_infinite(x)
        & Q.positive_infinite(y)) is False
    assert ask(Q.finite(a), Q.positive_infinite(x) & ~Q.finite(y)
        & ~Q.extended_positive(y)) is None
    assert ask(Q.finite(a), ~Q.finite(x) & ~Q.extended_positive(x)
        & Q.positive_infinite(y)) is None
    assert ask(Q.finite(a), ~Q.finite(x) & ~Q.finite(y)
        & ~Q.extended_positive(x) & ~Q.extended_positive(y)) is False
    # U + ?
    assert ask(Q.finite(a), ~Q.finite(y)) is None
    assert ask(Q.finite(a), Q.extended_positive(x)
        & ~Q.finite(y)) is None
    assert ask(Q.finite(a), Q.positive_infinite(y)) is None
    assert ask(Q.finite(a), Q.extended_positive(x)
        & Q.positive_infinite(y)) is False
    assert ask(Q.finite(a), Q.extended_positive(x)
        & ~Q.finite(y) & ~Q.extended_positive(y)) is None
    assert ask(Q.finite(a), ~Q.extended_positive(x)
        & Q.positive_infinite(y)) is None
    assert ask(Q.finite(a), ~Q.extended_positive(x) & ~Q.finite(y)
        & ~Q.extended_positive(y)) is False
    # ? + ?
    assert ask(Q.finite(a)) is None
    assert ask(Q.finite(a), Q.extended_positive(x)) is None
    assert ask(Q.finite(a), Q.extended_positive(y)) is None
    assert ask(Q.finite(a), Q.extended_positive(x)
        & Q.extended_positive(y)) is None
    assert ask(Q.finite(a), Q.extended_positive(x)
        & ~Q.extended_positive(y)) is None
    assert ask(Q.finite(a), ~Q.extended_positive(x)
        & Q.extended_positive(y)) is None
    assert ask(Q.finite(a), ~Q.extended_positive(x)
        & ~Q.extended_positive(y)) is None

    x, y, z = symbols('x,y,z')
    a = x + y + z
    x, y, z = a.args
    assert ask(Q.finite(a), Q.negative(x) & Q.negative(y)
        & Q.negative(z)) is True
    assert ask(Q.finite(a), Q.negative(x) & Q.negative(y)
        & Q.finite(z)) is True
    assert ask(Q.finite(a), Q.negative(x) & Q.negative(y)
        & Q.positive(z)) is True
    assert ask(Q.finite(a), Q.negative(x) & Q.negative(y)
        & Q.negative_infinite(z)) is False
    assert ask(Q.finite(a), Q.negative(x) & Q.negative(y)
        & ~Q.finite(z)) is False
    assert ask(Q.finite(a), Q.negative(x) & Q.negative(y)
        & Q.positive_infinite(z)) is False
    assert ask(Q.finite(a), Q.negative(x) & Q.negative(y)
        & Q.extended_negative(z)) is None
    assert ask(Q.finite(a), Q.negative(x) & Q.negative(y)) is None
    assert ask(Q.finite(a), Q.negative(x) & Q.negative(y)
        & Q.extended_positive(z)) is None
    assert ask(Q.finite(a), Q.negative(x) & Q.finite(y)
        & Q.finite(z)) is True
    assert ask(Q.finite(a), Q.negative(x) & Q.finite(y)
        & Q.positive(z)) is True
    assert ask(Q.finite(a), Q.negative(x) & Q.finite(y)
        & Q.negative_infinite(z)) is False
    assert ask(Q.finite(a), Q.negative(x) & Q.finite(y)
        & ~Q.finite(z)) is False
    assert ask(Q.finite(a), Q.negative(x) & Q.finite(y)
        & Q.positive_infinite(z)) is False
    assert ask(Q.finite(a), Q.negative(x) & Q.finite(y)
        & Q.extended_negative(z)) is None
    assert ask(Q.finite(a), Q.negative(x) & Q.finite(y)) is None
    assert ask(Q.finite(a), Q.negative(x) & Q.finite(y)
        & Q.extended_positive(z)) is None
    assert ask(Q.finite(a), Q.negative(x) & Q.positive(y)
        & Q.positive(z)) is True
    assert ask(Q.finite(a), Q.negative(x) & Q.positive(y)
        & Q.negative_infinite(z)) is False
    assert ask(Q.finite(a), Q.negative(x) & Q.positive(y)
        & ~Q.finite(z)) is False
    assert ask(Q.finite(a), Q.negative(x) & Q.positive(y)
        & Q.positive_infinite(z)) is False
    assert ask(Q.finite(a), Q.negative(x) & Q.positive(y)
        & Q.extended_negative(z)) is None
    assert ask(Q.finite(a), Q.negative(x) & Q.extended_positive(y)
        & Q.finite(y)) is None
    assert ask(Q.finite(a), Q.negative(x) & Q.positive(y)
        & Q.extended_positive(z)) is None
    assert ask(Q.finite(a), Q.negative(x) & Q.negative_infinite(y)
        & Q.negative_infinite(z)) is False
    assert ask(Q.finite(a), Q.negative(x) & Q.negative_infinite(y)
        & ~Q.finite(z)) is None
    assert ask(Q.finite(a), Q.negative(x) & Q.negative_infinite(y)
        & Q.positive_infinite(z)) is None
    assert ask(Q.finite(a), Q.negative(x) & Q.negative_infinite(y)
        & Q.extended_negative(z)) is False
    assert ask(Q.finite(a), Q.negative(x)
        & Q.negative_infinite(y)) is None
    assert ask(Q.finite(a), Q.negative(x) & Q.negative_infinite(y)
        & Q.extended_positive(z)) is None
    assert ask(Q.finite(a), Q.negative(x) & ~Q.finite(y)
        & ~Q.finite(z)) is None
    assert ask(Q.finite(a), Q.negative(x) & ~Q.finite(y)
        & Q.positive_infinite(z)) is None
    assert ask(Q.finite(a), Q.negative(x) & ~Q.finite(y)
        & Q.extended_negative(z)) is None
    assert ask(Q.finite(a), Q.negative(x) & ~Q.finite(y)) is None
    assert ask(Q.finite(a), Q.negative(x) & ~Q.finite(y)
        & Q.extended_positive(z)) is None
    assert ask(Q.finite(a), Q.negative(x) & Q.positive_infinite(y)
        & Q.positive_infinite(z)) is False
    assert ask(Q.finite(a), Q.negative(x) & Q.positive_infinite(y)
        & Q.negative_infinite(z)) is None
    assert ask(Q.finite(a), Q.negative(x) &
         Q.positive_infinite(y)) is None
    assert ask(Q.finite(a), Q.negative(x) & Q.positive_infinite(y)
        & Q.extended_positive(z)) is False
    assert ask(Q.finite(a), Q.negative(x) & Q.extended_negative(y)
        & Q.extended_negative(z)) is None
    assert ask(Q.finite(a), Q.negative(x)
        & Q.extended_negative(y)) is None
    assert ask(Q.finite(a), Q.negative(x) & Q.extended_negative(y)
        & Q.extended_positive(z)) is None
    assert ask(Q.finite(a), Q.negative(x)) is None
    assert ask(Q.finite(a), Q.negative(x)
        & Q.extended_positive(z)) is None
    assert ask(Q.finite(a), Q.negative(x) & Q.extended_positive(y)
        & Q.extended_positive(z)) is None
    assert ask(Q.finite(a), Q.finite(x) & Q.finite(y)
        & Q.finite(z)) is True
    assert ask(Q.finite(a), Q.finite(x) & Q.finite(y)
        & Q.positive(z)) is True
    assert ask(Q.finite(a), Q.finite(x) & Q.finite(y)
        & Q.negative_infinite(z)) is False
    assert ask(Q.finite(a), Q.finite(x) & Q.finite(y)
        & ~Q.finite(z)) is False
    assert ask(Q.finite(a), Q.finite(x) & Q.finite(y)
        & Q.positive_infinite(z)) is False
    assert ask(Q.finite(a), Q.finite(x) & Q.finite(y)
        & Q.extended_negative(z)) is None
    assert ask(Q.finite(a), Q.finite(x) & Q.finite(y)) is None
    assert ask(Q.finite(a), Q.finite(x) & Q.finite(y)
        & Q.extended_positive(z)) is None
    assert ask(Q.finite(a), Q.finite(x) & Q.positive(y)
        & Q.positive(z)) is True
    assert ask(Q.finite(a), Q.finite(x) & Q.positive(y)
        & Q.negative_infinite(z)) is False
    assert ask(Q.finite(a), Q.finite(x) & Q.positive(y)
        & ~Q.finite(z)) is False
    assert ask(Q.finite(a), Q.finite(x) & Q.positive(y)
        & Q.positive_infinite(z)) is False
    assert ask(Q.finite(a), Q.finite(x) & Q.positive(y)
        & Q.extended_negative(z)) is None
    assert ask(Q.finite(a), Q.finite(x) & Q.positive(y)) is None
    assert ask(Q.finite(a), Q.finite(x) & Q.positive(y)
        & Q.extended_positive(z)) is None
    assert ask(Q.finite(a), Q.finite(x) & Q.negative_infinite(y)
        & Q.negative_infinite(z)) is False
    assert ask(Q.finite(a), Q.finite(x) & Q.negative_infinite(y)
        & ~Q.finite(z)) is None
    assert ask(Q.finite(a), Q.finite(x) & Q.negative_infinite(y)
        & Q.positive_infinite(z)) is None
    assert ask(Q.finite(a), Q.finite(x) & Q.negative_infinite(y)
        & Q.extended_negative(z)) is False
    assert ask(Q.finite(a), Q.finite(x)
        & Q.negative_infinite(y)) is None
    assert ask(Q.finite(a), Q.finite(x) & Q.negative_infinite(y)
        & Q.extended_positive(z)) is None
    assert ask(Q.finite(a), Q.finite(x) & ~Q.finite(y)
        & ~Q.finite(z)) is None
    assert ask(Q.finite(a), Q.finite(x) & ~Q.finite(y)
        & Q.positive_infinite(z)) is None
    assert ask(Q.finite(a), Q.finite(x) & ~Q.finite(y)
        & Q.extended_negative(z)) is None
    assert ask(Q.finite(a), Q.finite(x) & ~Q.finite(y)) is None
    assert ask(Q.finite(a), Q.finite(x) & ~Q.finite(y)
        & Q.extended_positive(z)) is None
    assert ask(Q.finite(a), Q.finite(x) & Q.positive_infinite(y)
        & Q.positive_infinite(z)) is False
    assert ask(Q.finite(a), Q.finite(x) & Q.positive_infinite(y)
        & Q.extended_negative(z)) is None
    assert ask(Q.finite(a), Q.finite(x)
        & Q.positive_infinite(y)) is None
    assert ask(Q.finite(a), Q.finite(x) & Q.positive_infinite(y)
        & Q.extended_positive(z)) is False
    assert ask(Q.finite(a), Q.finite(x) & Q.extended_negative(y)
        & Q.extended_negative(z)) is None
    assert ask(Q.finite(a), Q.finite(x)
        & Q.extended_negative(y)) is None
    assert ask(Q.finite(a), Q.finite(x) & Q.extended_negative(y)
        & Q.extended_positive(z)) is None
    assert ask(Q.finite(a), Q.finite(x)) is None
    assert ask(Q.finite(a), Q.finite(x)
        & Q.extended_positive(z)) is None
    assert ask(Q.finite(a), Q.finite(x) & Q.extended_positive(y)
        & Q.extended_positive(z)) is None
    assert ask(Q.finite(a), Q.positive(x) & Q.positive(y)
        & Q.positive(z)) is True
    assert ask(Q.finite(a), Q.positive(x) & Q.positive(y)
        & Q.negative_infinite(z)) is False
    assert ask(Q.finite(a), Q.positive(x) & Q.positive(y)
        & ~Q.finite(z)) is False
    assert ask(Q.finite(a), Q.positive(x) & Q.positive(y)
        & Q.positive_infinite(z)) is False
    assert ask(Q.finite(a), Q.positive(x) & Q.positive(y)
        & Q.extended_negative(z)) is None
    assert ask(Q.finite(a), Q.positive(x) & Q.positive(y)) is None
    assert ask(Q.finite(a), Q.positive(x) & Q.positive(y)
        & Q.extended_positive(z)) is None
    assert ask(Q.finite(a), Q.positive(x) & Q.negative_infinite(y)
        & Q.negative_infinite(z)) is False
    assert ask(Q.finite(a), Q.positive(x) & Q.negative_infinite(y)
        & ~Q.finite(z)) is None
    assert ask(Q.finite(a), Q.positive(x) & Q.negative_infinite(y)
        & Q.positive_infinite(z)) is None
    assert ask(Q.finite(a), Q.positive(x) & Q.negative_infinite(y)
        & Q.extended_negative(z)) is False
    assert ask(Q.finite(a), Q.positive(x)
        & Q.negative_infinite(y)) is None
    assert ask(Q.finite(a), Q.positive(x) & Q.negative_infinite(y)
        & Q.extended_positive(z)) is None
    assert ask(Q.finite(a), Q.positive(x) & ~Q.finite(y)
        & ~Q.finite(z)) is None
    assert ask(Q.finite(a), Q.positive(x) & ~Q.finite(y)
        & Q.positive_infinite(z)) is None
    assert ask(Q.finite(a), Q.positive(x) & ~Q.finite(y)
        & Q.extended_negative(z)) is None
    assert ask(Q.finite(a), Q.positive(x) & ~Q.finite(y)) is None
    assert ask(Q.finite(a), Q.positive(x) & ~Q.finite(y)
        & Q.extended_positive(z)) is None
    assert ask(Q.finite(a), Q.positive(x) & Q.positive_infinite(y)
        & Q.positive_infinite(z)) is False
    assert ask(Q.finite(a), Q.positive(x) & Q.positive_infinite(y)
        & Q.extended_negative(z)) is None
    assert ask(Q.finite(a), Q.positive(x)
        & Q.positive_infinite(y)) is None
    assert ask(Q.finite(a), Q.positive(x) & Q.positive_infinite(y)
        & Q.extended_positive(z)) is False
    assert ask(Q.finite(a), Q.positive(x) & Q.extended_negative(y)
        & Q.extended_negative(z)) is None
    assert ask(Q.finite(a), Q.positive(x)
        & Q.extended_negative(y)) is None
    assert ask(Q.finite(a), Q.positive(x) & Q.extended_negative(y)
        & Q.extended_positive(z)) is None
    assert ask(Q.finite(a), Q.positive(x)) is None
    assert ask(Q.finite(a), Q.positive(x)
        & Q.extended_positive(z)) is None
    assert ask(Q.finite(a), Q.positive(x) & Q.extended_positive(y)
        & Q.extended_positive(z)) is None
    assert ask(Q.finite(a), Q.negative_infinite(x)
        & Q.negative_infinite(y) & Q.negative_infinite(z)) is False
    assert ask(Q.finite(a), Q.negative_infinite(x)
        & Q.negative_infinite(y) & ~Q.finite(z)) is None
    assert ask(Q.finite(a), Q.negative_infinite(x)
        & Q.negative_infinite(y)& Q.positive_infinite(z)) is None
    assert ask(Q.finite(a), Q.negative_infinite(x)
        & Q.negative_infinite(y) & Q.extended_negative(z)) is False
    assert ask(Q.finite(a), Q.negative_infinite(x)
        & Q.negative_infinite(y)) is None
    assert ask(Q.finite(a), Q.negative_infinite(x)
        & Q.negative_infinite(y) & Q.extended_positive(z)) is None
    assert ask(Q.finite(a), Q.negative_infinite(x)
        & ~Q.finite(y) & ~Q.finite(z)) is None
    assert ask(Q.finite(a), Q.negative_infinite(x)
        & ~Q.finite(y) & Q.positive_infinite(z)) is None
    assert ask(Q.finite(a), Q.negative_infinite(x)
        & ~Q.finite(y) & Q.extended_negative(z)) is None
    assert ask(Q.finite(a), Q.negative_infinite(x)
        & ~Q.finite(y)) is None
    assert ask(Q.finite(a), Q.negative_infinite(x)
        & ~Q.finite(y) & Q.extended_positive(z)) is None
    assert ask(Q.finite(a), Q.negative_infinite(x)
        & Q.positive_infinite(y) & Q.positive_infinite(z)) is None
    assert ask(Q.finite(a), Q.negative_infinite(x)
        & Q.positive_infinite(y) & Q.extended_negative(z)) is None
    assert ask(Q.finite(a), Q.negative_infinite(x)
        & Q.positive_infinite(y)) is None
    assert ask(Q.finite(a), Q.negative_infinite(x)
        & Q.positive_infinite(y) & Q.extended_positive(z)) is None
    assert ask(Q.finite(a), Q.negative_infinite(x)
        & Q.extended_negative(y) & Q.extended_negative(z)) is False
    assert ask(Q.finite(a), Q.negative_infinite(x)
        & Q.extended_negative(y)) is None
    assert ask(Q.finite(a), Q.negative_infinite(x)
        & Q.extended_negative(y) & Q.extended_positive(z)) is None
    assert ask(Q.finite(a), Q.negative_infinite(x)) is None
    assert ask(Q.finite(a), Q.negative_infinite(x)
        & Q.extended_positive(z)) is None
    assert ask(Q.finite(a), Q.negative_infinite(x)
        & Q.extended_positive(y) & Q.extended_positive(z)) is None
    assert ask(Q.finite(a), ~Q.finite(x) & ~Q.finite(y)
        & ~Q.finite(z)) is None
    assert ask(Q.finite(a), ~Q.finite(x) & Q.positive_infinite(z)
        & ~Q.finite(z)) is None
    assert ask(Q.finite(a), ~Q.finite(x) & ~Q.finite(y)
        & Q.extended_negative(z)) is None
    assert ask(Q.finite(a), ~Q.finite(x) & ~Q.finite(y)) is None
    assert ask(Q.finite(a), ~Q.finite(x) & ~Q.finite(y)
        & Q.extended_positive(z)) is None
    assert ask(Q.finite(a), ~Q.finite(x) & Q.positive_infinite(y)
        & Q.positive_infinite(z)) is None
    assert ask(Q.finite(a), ~Q.finite(x) & Q.positive_infinite(y)
        & Q.extended_negative(z)) is None
    assert ask(Q.finite(a), ~Q.finite(x)
        & Q.positive_infinite(y)) is None
    assert ask(Q.finite(a), ~Q.finite(x) & Q.positive_infinite(y)
        & Q.extended_positive(z)) is None
    assert ask(Q.finite(a), ~Q.finite(x) & Q.extended_negative(y)
        & Q.extended_negative(z)) is None
    assert ask(Q.finite(a), ~Q.finite(x)
        & Q.extended_negative(y)) is None
    assert ask(Q.finite(a), ~Q.finite(x) & Q.extended_negative(y)
        & Q.extended_positive(z)) is None
    assert ask(Q.finite(a), ~Q.finite(x)) is None
    assert ask(Q.finite(a), ~Q.finite(x)
        & Q.extended_positive(z)) is None
    assert ask(Q.finite(a), ~Q.finite(x) & Q.extended_positive(y)
        & Q.extended_positive(z)) is None
    assert ask(Q.finite(a), Q.positive_infinite(x)
        & Q.positive_infinite(y) & Q.positive_infinite(z)) is False
    assert ask(Q.finite(a), Q.positive_infinite(x)
        & Q.positive_infinite(y) & Q.extended_negative(z)) is None
    assert ask(Q.finite(a), Q.positive_infinite(x)
        & Q.positive_infinite(y)) is None
    assert ask(Q.finite(a), Q.positive_infinite(x)
        & Q.positive_infinite(y) & Q.extended_positive(z)) is False
    assert ask(Q.finite(a), Q.positive_infinite(x)
        & Q.extended_negative(y) & Q.extended_negative(z)) is None
    assert ask(Q.finite(a), Q.positive_infinite(x)
        & Q.extended_negative(y)) is None
    assert ask(Q.finite(a), Q.positive_infinite(x)
        & Q.extended_negative(y) & Q.extended_positive(z)) is None
    assert ask(Q.finite(a), Q.positive_infinite(x)) is None
    assert ask(Q.finite(a), Q.positive_infinite(x)
        & Q.extended_positive(z)) is None
    assert ask(Q.finite(a), Q.positive_infinite(x)
        & Q.extended_positive(y) & Q.extended_positive(z)) is False
    assert ask(Q.finite(a), Q.extended_negative(x)
        & Q.extended_negative(y) & Q.extended_negative(z)) is None
    assert ask(Q.finite(a), Q.extended_negative(x)
        & Q.extended_negative(y)) is None
    assert ask(Q.finite(a), Q.extended_negative(x)
        & Q.extended_negative(y) & Q.extended_positive(z)) is None
    assert ask(Q.finite(a), Q.extended_negative(x)) is None
    assert ask(Q.finite(a), Q.extended_negative(x)
        & Q.extended_positive(z)) is None
    assert ask(Q.finite(a), Q.extended_negative(x)
        & Q.extended_positive(y) & Q.extended_positive(z)) is None
    assert ask(Q.finite(a)) is None
    assert ask(Q.finite(a), Q.extended_positive(z)) is None
    assert ask(Q.finite(a), Q.extended_positive(y)
        & Q.extended_positive(z)) is None
    assert ask(Q.finite(a), Q.extended_positive(x)
        & Q.extended_positive(y) & Q.extended_positive(z)) is None

    assert ask(Q.finite(2*x)) is None
    assert ask(Q.finite(2*x), Q.finite(x)) is True

    x, y, z = symbols('x,y,z')
    a = x*y
    x, y = a.args
    assert ask(Q.finite(a), Q.finite(x) & Q.finite(y)) is True
    assert ask(Q.finite(a), Q.finite(x) & ~Q.zero(x) & ~Q.finite(y)) is False
    assert ask(Q.finite(a), Q.finite(x)) is None
    assert ask(Q.finite(a), ~Q.finite(x) & Q.finite(y) &~Q.zero(y)) is False
    assert ask(Q.finite(a), ~Q.finite(x) & ~Q.finite(y)) is False
    assert ask(Q.finite(a), ~Q.finite(x)) is None
    assert ask(Q.finite(a), Q.finite(y)) is None
    assert ask(Q.finite(a), ~Q.finite(y)) is None
    assert ask(Q.finite(a)) is None
    a = x*y*z
    x, y, z = a.args
    assert ask(Q.finite(a), Q.finite(x) & Q.finite(y)
        & Q.finite(z)) is True
    assert ask(Q.finite(a), Q.finite(x) & ~Q.zero(x) & Q.finite(y)
        & ~Q.zero(y) & ~Q.finite(z)) is False
    assert ask(Q.finite(a), Q.finite(x) & Q.finite(y)) is None
    assert ask(Q.finite(a), Q.finite(x) & ~Q.zero(x) & ~Q.finite(y)
        & Q.finite(z) & ~Q.zero(z)) is False
    assert ask(Q.finite(a), Q.finite(x) & ~Q.zero(x) & ~Q.finite(y)
        & ~Q.finite(z)) is False
    assert ask(Q.finite(a), Q.finite(x) & ~Q.finite(y)) is None
    assert ask(Q.finite(a), Q.finite(x) & Q.finite(z)) is None
    assert ask(Q.finite(a), Q.finite(x) & ~Q.finite(z)) is None
    assert ask(Q.finite(a), Q.finite(x)) is None
    assert ask(Q.finite(a), ~Q.finite(x) & Q.finite(y) & ~Q.zero(y)
        & Q.finite(z) & ~Q.zero(z)) is False
    assert ask(Q.finite(a), ~Q.finite(x) & ~Q.zero(x) & Q.finite(y)
        & ~Q.zero(y) & ~Q.finite(z)) is False
    assert ask(Q.finite(a), ~Q.finite(x) & Q.finite(y)) is None
    assert ask(Q.finite(a), ~Q.finite(x) & ~Q.finite(y)
        & Q.finite(z) & ~Q.zero(z)) is False
    assert ask(Q.finite(a), ~Q.finite(x) & ~Q.finite(y)
        & ~Q.finite(z)) is False
    assert ask(Q.finite(a), ~Q.finite(x) & ~Q.finite(y)) is None
    assert ask(Q.finite(a), ~Q.finite(x) & Q.finite(z)) is None
    assert ask(Q.finite(a), ~Q.finite(x) & ~Q.finite(z)) is None
    assert ask(Q.finite(a), ~Q.finite(x)) is None
    assert ask(Q.finite(a), Q.finite(y) & Q.finite(z)) is None
    assert ask(Q.finite(a), Q.finite(y) & ~Q.finite(z)) is None
    assert ask(Q.finite(a), Q.finite(y)) is None
    assert ask(Q.finite(a), ~Q.finite(y) & Q.finite(z)) is None
    assert ask(Q.finite(a), ~Q.finite(y) & ~Q.finite(z)) is None
    assert ask(Q.finite(a), ~Q.finite(y)) is None
    assert ask(Q.finite(a), Q.finite(z)) is None
    assert ask(Q.finite(a), ~Q.finite(z)) is None
    assert ask(Q.finite(a), ~Q.finite(z) & Q.extended_nonzero(x)
        & Q.extended_nonzero(y) & Q.extended_nonzero(z)) is None
    assert ask(Q.finite(a), Q.extended_nonzero(x) & ~Q.finite(y)
        & Q.extended_nonzero(y) & ~Q.finite(z)
        & Q.extended_nonzero(z)) is False

    x, y, z = symbols('x,y,z')
    assert ask(Q.finite(x**2)) is None
    assert ask(Q.finite(2**x)) is None
    assert ask(Q.finite(2**x), Q.finite(x)) is True
    assert ask(Q.finite(x**x)) is None
    assert ask(Q.finite(S.Half ** x)) is None
    assert ask(Q.finite(S.Half ** x), Q.extended_positive(x)) is True
    assert ask(Q.finite(S.Half ** x), Q.extended_negative(x)) is None
    assert ask(Q.finite(2**x), Q.extended_negative(x)) is True
    assert ask(Q.finite(sqrt(x))) is None
    assert ask(Q.finite(2**x), ~Q.finite(x)) is False
    assert ask(Q.finite(x**2), ~Q.finite(x)) is False

    # https://github.com/sympy/sympy/issues/27707
    assert ask(Q.finite(x**y), Q.real(x) & Q.real(y)) is None
    assert ask(Q.finite(x**y), Q.real(x) & Q.negative(y)) is None
    assert ask(Q.finite(x**y), Q.zero(x) & Q.negative(y)) is False
    assert ask(Q.finite(x**y), Q.real(x) & Q.positive(y)) is True
    assert ask(Q.finite(x**y), Q.nonzero(x) & Q.real(y)) is True
    assert ask(Q.finite(x**y), Q.nonzero(x) & Q.negative(y)) is True
    assert ask(Q.finite(x**y), Q.zero(x) & Q.positive(y)) is True

    # sign function
    assert ask(Q.finite(sign(x))) is True
    assert ask(Q.finite(sign(x)), ~Q.finite(x)) is True

    # exponential functions
    assert ask(Q.finite(log(x))) is None
    assert ask(Q.finite(log(x)), Q.finite(x)) is None
    assert ask(Q.finite(log(x)), ~Q.zero(x)) is True
    assert ask(Q.finite(log(x)), Q.infinite(x)) is False
    assert ask(Q.finite(log(x)), Q.zero(x)) is False
    assert ask(Q.finite(exp(x))) is None
    assert ask(Q.finite(exp(x)), Q.finite(x)) is True
    assert ask(Q.finite(exp(2))) is True

    # trigonometric functions
    assert ask(Q.finite(sin(x))) is True
    assert ask(Q.finite(sin(x)), ~Q.finite(x)) is True
    assert ask(Q.finite(cos(x))) is True
    assert ask(Q.finite(cos(x)), ~Q.finite(x)) is True
    assert ask(Q.finite(2*sin(x))) is True
    assert ask(Q.finite(sin(x)**2)) is True
    assert ask(Q.finite(cos(x)**2)) is True
    assert ask(Q.finite(cos(x) + sin(x))) is True

