
def test_Number_cmp():
    n1 = Number(1)
    n2 = Number(2)
    n3 = Number(-3)

    assert n1 < n2
    assert n1 <= n2
    assert n3 < n1
    assert n2 > n3
    assert n2 >= n3

    raises(TypeError, lambda: n1 < S.NaN)
    raises(TypeError, lambda: n1 <= S.NaN)
    raises(TypeError, lambda: n1 > S.NaN)
    raises(TypeError, lambda: n1 >= S.NaN)

