
def test_pos_neg():
    assert satask(~Q.positive(x), Q.negative(x)) is True
    assert satask(~Q.negative(x), Q.positive(x)) is True
    assert satask(Q.positive(x + y), Q.positive(x) & Q.positive(y)) is True
    assert satask(Q.negative(x + y), Q.negative(x) & Q.negative(y)) is True
    assert satask(Q.positive(x + y), Q.negative(x) & Q.negative(y)) is False
    assert satask(Q.negative(x + y), Q.positive(x) & Q.positive(y)) is False

