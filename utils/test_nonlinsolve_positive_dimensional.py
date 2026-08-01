
def test_nonlinsolve_positive_dimensional():
    x, y, a, b, c, d = symbols('x, y, a, b, c, d', extended_real=True)
    assert nonlinsolve([x*y, x*y - x], [x, y]) == FiniteSet((0, y))

    system = [a**2 + a*c, a - b]
    assert nonlinsolve(system, [a, b]) == FiniteSet((0, 0), (-c, -c))
    # here (a= 0, b = 0) is independent soln so both is printed.
    # if symbols = [a, b, c] then only {a : -c ,b : -c}

    eq1 =  a + b + c + d
    eq2 = a*b + b*c + c*d + d*a
    eq3 = a*b*c + b*c*d + c*d*a + d*a*b
    eq4 = a*b*c*d - 1
    system = [eq1, eq2, eq3, eq4]
    sol1 = (-1/d, -d, 1/d, FiniteSet(d) - FiniteSet(0))
    sol2 = (1/d, -d, -1/d, FiniteSet(d) - FiniteSet(0))
    soln = FiniteSet(sol1, sol2)
    assert nonlinsolve(system, [a, b, c, d]) == soln

    assert nonlinsolve([x**4 - 3*x**2 + y*x, x*z**2, y*z - 1], [x, y, z]) == \
           {(0, 1/z, z)}

