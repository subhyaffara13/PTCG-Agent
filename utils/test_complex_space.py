
def test_complex_space():
    c1 = ComplexSpace(2)
    assert isinstance(c1, ComplexSpace)
    assert c1.dimension == 2
    assert sstr(c1) == 'C(2)'
    assert srepr(c1) == 'ComplexSpace(Integer(2))'

    n = Symbol('n')
    c2 = ComplexSpace(n)
    assert isinstance(c2, ComplexSpace)
    assert c2.dimension == n
    assert sstr(c2) == 'C(n)'
    assert srepr(c2) == "ComplexSpace(Symbol('n'))"
    assert c2.subs(n, 2) == ComplexSpace(2)

