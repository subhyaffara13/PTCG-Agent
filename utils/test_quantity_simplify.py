
def test_quantity_simplify():
    from sympy.physics.units.util import quantity_simplify
    from sympy.physics.units import kilo, foot
    from sympy.core.symbol import symbols

    x, y = symbols('x y')

    assert quantity_simplify(x*(8*kilo*newton*meter + y)) == x*(8000*meter*newton + y)
    assert quantity_simplify(foot*inch*(foot + inch)) == foot**2*(foot + foot/12)/12
    assert quantity_simplify(foot*inch*(foot*foot + inch*(foot + inch))) == foot**2*(foot**2 + foot/12*(foot + foot/12))/12
    assert quantity_simplify(2**(foot/inch*kilo/1000)*inch) == 4096*foot/12
    assert quantity_simplify(foot**2*inch + inch**2*foot) == 13*foot**3/144

