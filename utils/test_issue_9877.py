
def test_issue_9877():
    ucode_str1 = '(2, 3) ∪ ([1, 2] \\ {x})'
    a, b, c = Interval(2, 3, True, True), Interval(1, 2), FiniteSet(x)
    assert upretty(Union(a, Complement(b, c))) == ucode_str1

    ucode_str2 = '{x} ∩ {y} ∩ ({z} \\ [1, 2])'
    d, e, f, g = FiniteSet(x), FiniteSet(y), FiniteSet(z), Interval(1, 2)
    assert upretty(Intersection(d, e, Complement(f, g))) == ucode_str2

