
def test_issue_10426():
    x = Dummy('x')
    a = Symbol('a')
    n = Dummy('n')
    assert (solveset(sin(x + a) - sin(x), a)).dummy_eq(Dummy('x')) == (Union(
        ImageSet(Lambda(n, 2*n*pi), S.Integers),
        Intersection(S.Complexes, ImageSet(Lambda(n, -I*(I*(2*n*pi + arg(-exp(-2*I*x))) + 2*im(x))),
        S.Integers)))).dummy_eq(Dummy('x,n'))

