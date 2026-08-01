
def test_issue_23718():
    f = 1/(b*cos(x) + a*sin(x))
    Fpos = (-log(-a/b + tan(x/2) - sqrt(a**2 + b**2)/b)/sqrt(a**2 + b**2)
            +log(-a/b + tan(x/2) + sqrt(a**2 + b**2)/b)/sqrt(a**2 + b**2))
    F = Piecewise(
        # XXX: The zoo case here is for a=b=0 so it should just be zoo or maybe
        # it doesn't really need to be included at all given that the original
        # integrand is really undefined in that case anyway.
        (zoo*(-log(tan(x/2) - 1) + log(tan(x/2) + 1)),  Eq(a, 0) & Eq(b, 0)),
        (log(tan(x/2))/a,                               Eq(b, 0)),
        (-I/(-I*b*sin(x) + b*cos(x)),                   Eq(a, -I*b)),
        (I/(I*b*sin(x) + b*cos(x)),                     Eq(a,  I*b)),
        (Fpos,                                          True),
    )
    assert integrate(f, x) == F

    ap, bp = symbols('a, b', positive=True)
    rep = {a: ap, b: bp}
    assert integrate(f.subs(rep), x) == Fpos.subs(rep)

