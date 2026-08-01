
def test_gateinputcount():
    a, b, c, d, e = symbols('a:e')
    assert gateinputcount(And(a, b)) == 2
    assert gateinputcount(a | b & c & d ^ (e | a)) == 9
    assert gateinputcount(And(a, True)) == 0
    raises(TypeError, lambda: gateinputcount(a * b))

