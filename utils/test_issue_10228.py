
def test_issue_10228():
    assert cse([x*y**2 + x*y]) == ([(x0, x*y)], [x0*y + x0])
    assert cse([x + y, 2*x + y]) == ([(x0, x + y)], [x0, x + x0])
    assert cse((w + 2*x + y + z, w + x + 1)) == (
        [(x0, w + x)], [x0 + x + y + z, x0 + 1])
    assert cse(((w + x + y + z)*(w - x))/(w + x)) == (
        [(x0, w + x)], [(x0 + y + z)*(w - x)/x0])
    a, b, c, d, f, g, j, m = symbols('a, b, c, d, f, g, j, m')
    exprs = (d*g**2*j*m, 4*a*f*g*m, a*b*c*f**2)
    assert cse(exprs) == (
        [(x0, g*m), (x1, a*f)], [d*g*j*x0, 4*x0*x1, b*c*f*x1]
)

