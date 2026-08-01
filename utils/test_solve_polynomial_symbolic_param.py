
def test_solve_polynomial_symbolic_param():
    assert solveset_complex((x**2 - 1)**2 - a, x) == \
        FiniteSet(sqrt(1 + sqrt(a)), -sqrt(1 + sqrt(a)),
                  sqrt(1 - sqrt(a)), -sqrt(1 - sqrt(a)))

    # issue 4507
    assert solveset_complex(y - b/(1 + a*x), x) == \
        FiniteSet((b/y - 1)/a) - FiniteSet(-1/a)

    # issue 4508
    assert solveset_complex(y - b*x/(a + x), x) == \
        FiniteSet(-a*y/(y - b)) - FiniteSet(-a)

