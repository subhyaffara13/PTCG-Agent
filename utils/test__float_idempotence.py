
def test_Float_idempotence():
    x = Float('1.23', '')
    y = Float(x)
    z = Float(x, 15)
    assert same_and_same_prec(y, x)
    assert not same_and_same_prec(z, x)
    x = Float(10**20)
    y = Float(x)
    z = Float(x, 15)
    assert same_and_same_prec(y, x)
    assert not same_and_same_prec(z, x)

