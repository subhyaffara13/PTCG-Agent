
def test_trigsimp_issues():
    a, x, y = symbols('a x y')

    # issue 4625 - factor_terms works, too
    assert trigsimp(sin(x)**3 + cos(x)**2*sin(x)) == sin(x)

    # issue 5948
    assert trigsimp(diff(integrate(cos(x)/sin(x)**3, x), x)) == \
        cos(x)/sin(x)**3
    assert trigsimp(diff(integrate(sin(x)/cos(x)**3, x), x)) == \
        sin(x)/cos(x)**3

    # check integer exponents
    e = sin(x)**y/cos(x)**y
    assert trigsimp(e) == e
    assert trigsimp(e.subs(y, 2)) == tan(x)**2
    assert trigsimp(e.subs(x, 1)) == tan(1)**y

    # check for multiple patterns
    assert (cos(x)**2/sin(x)**2*cos(y)**2/sin(y)**2).trigsimp() == \
        1/tan(x)**2/tan(y)**2
    assert trigsimp(cos(x)/sin(x)*cos(x+y)/sin(x+y)) == \
        1/(tan(x)*tan(x + y))

    eq = cos(2)*(cos(3) + 1)**2/(cos(3) - 1)**2
    assert trigsimp(eq) == eq.factor()  # factor makes denom (-1 + cos(3))**2
    assert trigsimp(cos(2)*(cos(3) + 1)**2*(cos(3) - 1)**2) == \
        cos(2)*sin(3)**4

    # issue 6789; this generates an expression that formerly caused
    # trigsimp to hang
    assert cot(x).equals(tan(x)) is False

    # nan or the unchanged expression is ok, but not sin(1)
    z = cos(x)**2 + sin(x)**2 - 1
    z1 = tan(x)**2 - 1/cot(x)**2
    n = (1 + z1/z)
    assert trigsimp(sin(n)) != sin(1)
    eq = x*(n - 1) - x*n
    assert trigsimp(eq) is S.NaN
    assert trigsimp(eq, recursive=True) is S.NaN
    assert trigsimp(1).is_Integer

    assert trigsimp(-sin(x)**4 - 2*sin(x)**2*cos(x)**2 - cos(x)**4) == -1

