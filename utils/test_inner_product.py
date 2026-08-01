
def test_inner_product():
    i, j, k, l = symbols('i,j,k,l')
    s1 = BBra([0])
    s2 = BKet([1])
    assert InnerProduct(s1, Dagger(s1)) == 1
    assert InnerProduct(s1, s2) == 0
    s1 = BBra([i, j])
    s2 = BKet([k, l])
    r = InnerProduct(s1, s2)
    assert r == KroneckerDelta(i, k)*KroneckerDelta(j, l)

