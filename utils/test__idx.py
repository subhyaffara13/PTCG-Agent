
def test_Idx():
    # Issue 26888
    a = IndexedBase('a')
    i = Idx('i')
    b = [1,2,3]
    assert lambdify([a, i], a[i])(b, 2) == 3

