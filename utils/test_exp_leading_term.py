
def test_exp_leading_term():
    assert exp(x).as_leading_term(x) == 1
    assert exp(2 + x).as_leading_term(x) == exp(2)
    assert exp((2*x + 3) / (x+1)).as_leading_term(x) == exp(3)

