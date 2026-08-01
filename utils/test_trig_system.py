
def test_trig_system():
    # TODO: add more simple testcases when solveset returns
    # simplified soln for Trig eq
    assert nonlinsolve([sin(x) - 1, cos(x) -1 ], x) == S.EmptySet
    soln1 = (ImageSet(Lambda(n, 2*n*pi + pi/2), S.Integers),)
    soln = FiniteSet(soln1)
    assert dumeq(nonlinsolve([sin(x) - 1, cos(x)], x), soln)

