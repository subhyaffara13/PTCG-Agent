
def test_ComplexRegion_contains():
    r = Symbol('r', real=True)
    # contains in ComplexRegion
    a = Interval(2, 3)
    b = Interval(4, 6)
    c = Interval(7, 9)
    c1 = ComplexRegion(a*b)
    c2 = ComplexRegion(Union(a*b, c*a))
    assert 2.5 + 4.5*I in c1
    assert 2 + 4*I in c1
    assert 3 + 4*I in c1
    assert 8 + 2.5*I in c2
    assert 2.5 + 6.1*I not in c1
    assert 4.5 + 3.2*I not in c1
    assert c1.contains(x) == Contains(x, c1, evaluate=False)
    assert c1.contains(r) == False
    assert c2.contains(x) == Contains(x, c2, evaluate=False)
    assert c2.contains(r) == False

    r1 = Interval(0, 1)
    theta1 = Interval(0, 2*S.Pi)
    c3 = ComplexRegion(r1*theta1, polar=True)
    assert (0.5 + I*6/10) in c3
    assert (S.Half + I*6/10) in c3
    assert (S.Half + .6*I) in c3
    assert (0.5 + .6*I) in c3
    assert I in c3
    assert 1 in c3
    assert 0 in c3
    assert 1 + I not in c3
    assert 1 - I not in c3
    assert c3.contains(x) == Contains(x, c3, evaluate=False)
    assert c3.contains(r + 2*I) == Contains(
        r + 2*I, c3, evaluate=False)  # is in fact False
    assert c3.contains(1/(1 + r**2)) == Contains(
        1/(1 + r**2), c3, evaluate=False)  # is in fact True

    r2 = Interval(0, 3)
    theta2 = Interval(pi, 2*pi, left_open=True)
    c4 = ComplexRegion(r2*theta2, polar=True)
    assert c4.contains(0) == True
    assert c4.contains(2 + I) == False
    assert c4.contains(-2 + I) == False
    assert c4.contains(-2 - I) == True
    assert c4.contains(2 - I) == True
    assert c4.contains(-2) == False
    assert c4.contains(2) == True
    assert c4.contains(x) == Contains(x, c4, evaluate=False)
    assert c4.contains(3/(1 + r**2)) == Contains(
        3/(1 + r**2), c4, evaluate=False)  # is in fact True

    raises(ValueError, lambda: ComplexRegion(r1*theta1, polar=2))

