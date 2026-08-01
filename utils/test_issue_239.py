
def test_issue_239():
    mp.prec = 150
    x = ldexp(2476979795053773,-52)
    assert betainc(206, 385, 0, 0.55, 1).ae('0.99999999999999999999996570910644857895771110649954')
    mp.dps = 15
    pytest.raises(ValueError, lambda: hyp2f1(-5,5,0.5,0.5))

