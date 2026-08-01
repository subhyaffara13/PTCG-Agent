
def test_is_absolutely_convergent():
    assert Sum((-1)**n, (n, 1, oo)).is_absolutely_convergent() is S.false
    assert Sum((-1)**n/n**2, (n, 1, oo)).is_absolutely_convergent() is S.true

