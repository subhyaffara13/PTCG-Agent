
def test_anyarg():
    assert anyarg(x, Q.zero(x), x*y) == Or(Q.zero(x), Q.zero(y))
    assert anyarg(x, Q.positive(x) & Q.negative(x), x*y) == \
        Or(Q.positive(x) & Q.negative(x), Q.positive(y) & Q.negative(y))

