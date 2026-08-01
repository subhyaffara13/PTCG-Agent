
def test_Product_is_convergent():
    assert Product(1/n**2, (n, 1, oo)).is_convergent() is S.false
    assert Product(exp(1/n**2), (n, 1, oo)).is_convergent() is S.true
    assert Product(1/n, (n, 1, oo)).is_convergent() is S.false
    assert Product(1 + 1/n, (n, 1, oo)).is_convergent() is S.false
    assert Product(1 + 1/n**2, (n, 1, oo)).is_convergent() is S.true

