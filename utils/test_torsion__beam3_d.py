
def test_torsion_Beam3D():
    x = symbols('x')
    b = Beam3D(20, 40, 21, 100, 25)
    b.apply_moment_load(15, 5, -2, dir='x')
    b.apply_moment_load(25, 10, -2, dir='x')
    b.apply_moment_load(-5, 20, -2, dir='x')
    b.solve_for_torsion()
    assert b.angular_deflection().subs(x, 3) == sympify("1/40")
    assert b.angular_deflection().subs(x, 9) == sympify("17/280")
    assert b.angular_deflection().subs(x, 12) == sympify("53/840")
    assert b.angular_deflection().subs(x, 17) == sympify("2/35")
    assert b.angular_deflection().subs(x, 20) == sympify("3/56")

