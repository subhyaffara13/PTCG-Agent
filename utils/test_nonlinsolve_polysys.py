
def test_nonlinsolve_polysys():
    x, y, z = symbols('x, y, z', real=True)
    assert nonlinsolve([x**2 + y - 2, x**2 + y], [x, y]) == S.EmptySet

    s = (-y + 2, y)
    assert nonlinsolve([(x + y)**2 - 4, x + y - 2], [x, y]) == FiniteSet(s)

    system = [x**2 - y**2]
    soln_real = FiniteSet((-y, y), (y, y))
    soln_complex = FiniteSet((-Abs(y), y), (Abs(y), y))
    soln =soln_real + soln_complex
    assert nonlinsolve(system, [x, y]) == soln

    system = [x**2 - y**2]
    soln_real= FiniteSet((y, -y), (y, y))
    soln_complex = FiniteSet((y, -Abs(y)), (y, Abs(y)))
    soln = soln_real + soln_complex
    assert nonlinsolve(system, [y, x]) == soln

    system = [x**2 + y - 3, x - y - 4]
    assert nonlinsolve(system, (x, y)) != nonlinsolve(system, (y, x))

    assert nonlinsolve([-x**2 - y**2 + z, -2*x, -2*y, S.One], [x, y, z]) == S.EmptySet
    assert nonlinsolve([x + y + z, S.One, S.One, S.One], [x, y, z]) == S.EmptySet

    system = [-x**2*z**2 + x*y*z + y**4, -2*x*z**2 + y*z, x*z + 4*y**3, -2*x**2*z + x*y]
    assert nonlinsolve(system, [x, y, z]) == FiniteSet((0, 0, z), (x, 0, 0))

