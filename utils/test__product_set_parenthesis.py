
def test_ProductSet_parenthesis():
    ucode_str = '([4, 7] × {1, 2}) ∪ ([2, 3] × [4, 7])'

    a, b = Interval(2, 3), Interval(4, 7)
    assert upretty(Union(a*b, b*FiniteSet(1, 2))) == ucode_str

