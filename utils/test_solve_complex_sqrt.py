
def test_solve_complex_sqrt():
    assert solveset_complex(sqrt(5*x + 6) - 2 - x, x) == \
        FiniteSet(-S.One, S(2))
    assert solveset_complex(sqrt(5*x + 6) - (2 + 2*I) - x, x) == \
        FiniteSet(-S(2), 3 - 4*I)
    assert solveset_complex(4*x*(1 - a * sqrt(x)), x) == \
        FiniteSet(S.Zero, 1 / a ** 2)

