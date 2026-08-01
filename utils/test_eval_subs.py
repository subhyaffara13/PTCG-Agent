
def test_eval_subs():
    energy, mass, force = symbols('energy mass force')
    expr1 = energy/mass
    units = {energy: kilogram*meter**2/second**2, mass: kilogram}
    assert expr1.subs(units) == meter**2/second**2
    expr2 = force/mass
    units = {force:gravitational_constant*kilogram**2/meter**2, mass:kilogram}
    assert expr2.subs(units) == gravitational_constant*kilogram/meter**2

