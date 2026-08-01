
def test_allargs():
    assert allargs(x, Q.zero(x), x*y) == And(Q.zero(x), Q.zero(y))
    assert allargs(x, Q.positive(x) | Q.negative(x), x*y) == And(Q.positive(x) | Q.negative(x), Q.positive(y) | Q.negative(y))

