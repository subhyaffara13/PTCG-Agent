
def test_issue_12448():
    f = Function('f')
    fun = [f(i) for i in range(15)]
    sym = symbols('x:15')
    reps = dict(zip(fun, sym))

    (x, y, z), c = sym[:3], sym[3:]
    ssym = solve([c[4*i]*x + c[4*i + 1]*y + c[4*i + 2]*z + c[4*i + 3]
        for i in range(3)], (x, y, z))

    (x, y, z), c = fun[:3], fun[3:]
    sfun = solve([c[4*i]*x + c[4*i + 1]*y + c[4*i + 2]*z + c[4*i + 3]
        for i in range(3)], (x, y, z))

    assert sfun[fun[0]].xreplace(reps).count_ops() == \
        ssym[sym[0]].count_ops()

