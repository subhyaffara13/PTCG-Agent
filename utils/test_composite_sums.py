
def test_composite_sums():
    f = S.Half*(7 - 6*n + Rational(1, 7)*n**3)
    s = summation(f, (n, a, b))
    assert not isinstance(s, Sum)
    A = 0
    for i in range(-3, 5):
        A += f.subs(n, i)
    B = s.subs(a, -3).subs(b, 4)
    assert A == B

