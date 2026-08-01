
def test_issue_12645():
    x, y = symbols('x y', real=True)
    assert (integrate(sin(x*x*x + y*y),
                      (x, -sqrt(pi - y*y), sqrt(pi - y*y)),
                      (y, -sqrt(pi), sqrt(pi)))
                == Integral(sin(x**3 + y**2),
                            (x, -sqrt(-y**2 + pi), sqrt(-y**2 + pi)),
                            (y, -sqrt(pi), sqrt(pi))))

