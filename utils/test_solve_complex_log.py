
def test_solve_complex_log():
    assert solveset_complex(log(x), x) == FiniteSet(1)
    assert solveset_complex(1 - log(a + 4*x**2), x) == \
        FiniteSet(-sqrt(-a + E)/2, sqrt(-a + E)/2)

