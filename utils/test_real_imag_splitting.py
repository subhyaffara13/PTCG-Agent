
def test_real_imag_splitting():
    a, b = symbols('a b', real=True)
    assert solve(sqrt(a**2 + b**2) - 3, a) == \
        [-sqrt(-b**2 + 9), sqrt(-b**2 + 9)]
    a, b = symbols('a b', imaginary=True)
    assert solve(sqrt(a**2 + b**2) - 3, a) == []


def test_real_imag_splitting():
    a, b = symbols('a b', real=True)
    assert solveset_real(sqrt(a**2 - b**2) - 3, a) == \
        FiniteSet(-sqrt(b**2 + 9), sqrt(b**2 + 9))
    assert solveset_real(sqrt(a**2 + b**2) - 3, a) != \
        S.EmptySet

