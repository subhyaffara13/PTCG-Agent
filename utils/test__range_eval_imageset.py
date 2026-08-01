
def test_Range_eval_imageset():
    a, b, c = symbols('a b c')
    assert imageset(x, a*(x + b) + c, Range(3)) == \
        imageset(x, a*x + a*b + c, Range(3))
    eq = (x + 1)**2
    assert imageset(x, eq, Range(3)).lamda.expr == eq
    eq = a*(x + b) + c
    r = Range(3, -3, -2)
    imset = imageset(x, eq, r)
    assert imset.lamda.expr != eq
    assert list(imset) == [eq.subs(x, i).expand() for i in list(r)]

