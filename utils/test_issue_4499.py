
def test_issue_4499():
    # previously, this gave 16 constants
    from sympy.abc import a, b
    B = Function('B')
    G = Function('G')
    t = Tuple(*
        (a, a + S.Half, 2*a, b, 2*a - b + 1, (sqrt(z)/2)**(-2*a + 1)*B(2*a -
        b, sqrt(z))*B(b - 1, sqrt(z))*G(b)*G(2*a - b + 1),
        sqrt(z)*(sqrt(z)/2)**(-2*a + 1)*B(b, sqrt(z))*B(2*a - b,
        sqrt(z))*G(b)*G(2*a - b + 1), sqrt(z)*(sqrt(z)/2)**(-2*a + 1)*B(b - 1,
        sqrt(z))*B(2*a - b + 1, sqrt(z))*G(b)*G(2*a - b + 1),
        (sqrt(z)/2)**(-2*a + 1)*B(b, sqrt(z))*B(2*a - b + 1,
        sqrt(z))*G(b)*G(2*a - b + 1), 1, 0, S.Half, z/2, -b + 1, -2*a + b,
        -2*a))
    c = cse(t)
    ans = (
        [(x0, 2*a), (x1, -b + x0), (x2, x1 + 1), (x3, b - 1), (x4, sqrt(z)),
         (x5, B(x3, x4)), (x6, (x4/2)**(1 - x0)*G(b)*G(x2)), (x7, x6*B(x1, x4)),
         (x8, B(b, x4)), (x9, x6*B(x2, x4))],
        [(a, a + S.Half, x0, b, x2, x5*x7, x4*x7*x8, x4*x5*x9, x8*x9,
          1, 0, S.Half, z/2, -x3, -x1, -x0)])
    assert ans == c

