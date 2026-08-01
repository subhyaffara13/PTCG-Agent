
def test_issue_21882():

    a, b, c, d, f, g, k = unknowns = symbols('a, b, c, d, f, g, k')

    equations = [
        -k*a + b + 5*f/6 + 2*c/9 + 5*d/6 + 4*a/3,
        -k*f + 4*f/3 + d/2,
        -k*d + f/6 + d,
        13*b/18 + 13*c/18 + 13*a/18,
        -k*c + b/2 + 20*c/9 + a,
        -k*b + b + c/18 + a/6,
        5*b/3 + c/3 + a,
        2*b/3 + 2*c + 4*a/3,
        -g,
    ]

    answer = [
        {a: 0, f: 0, b: 0, d: 0, c: 0, g: 0},
        {a: 0, f: -d, b: 0, k: S(5)/6, c: 0, g: 0},
        {a: -2*c, f: 0, b: c, d: 0, k: S(13)/18, g: 0}]
    # but not {a: 0, f: 0, b: 0, k: S(3)/2, c: 0, d: 0, g: 0}
    # since this is already covered by the first solution
    got = solve(equations, unknowns, dict=True)
    assert got == answer, (got,answer)

