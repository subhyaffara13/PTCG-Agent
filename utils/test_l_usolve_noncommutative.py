
def test_LUsolve_noncommutative():
    a0, a1, a2, a3 = symbols("a:4", commutative=False)
    b0, b1 = symbols("b:2", commutative=False)
    A = Matrix([[a0, a1], [a2, a3]])
    check = A * A.LUsolve(Matrix([b0, b1]))
    assert check[0, 0].expand() == b0
    # Because sympy simplification is very limited with noncommutative expressions,
    # perform an explicit check with the second element
    assert check[1, 0] == (
        a2*a0**(-1)*(-a1*(-a2*a0**(-1)*a1 + a3)**(-1)*(-a2*a0**(-1)*b0 + b1) + b0)
        + a3*(-a2*a0**(-1)*a1 + a3)**(-1)*(-a2*a0**(-1)*b0 + b1)
    )

