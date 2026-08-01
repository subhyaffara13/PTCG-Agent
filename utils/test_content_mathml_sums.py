
def test_content_mathml_sums():
    summand = x
    mml_1 = mp._print(Sum(summand, (x, 1, 10)))
    assert mml_1.childNodes[0].nodeName == 'sum'
    assert mml_1.childNodes[1].nodeName == 'bvar'
    assert mml_1.childNodes[2].nodeName == 'lowlimit'
    assert mml_1.childNodes[3].nodeName == 'uplimit'
    assert mml_1.childNodes[4].toxml() == mp._print(summand).toxml()

