
def test_beam_units():
    E = Symbol('E')
    I = Symbol('I')
    R1, R2 = symbols('R1, R2')

    kN = kilo*newton
    gN = giga*newton

    b = Beam(8*meter, 200*gN/meter**2, 400*1000000*(milli*meter)**4)
    b.apply_load(5*kN, 2*meter, -1)
    b.apply_load(R1, 0*meter, -1)
    b.apply_load(R2, 8*meter, -1)
    b.apply_load(10*kN/meter, 4*meter, 0, end=8*meter)
    b.bc_deflection = [(0*meter, 0*meter), (8*meter, 0*meter)]
    b.solve_for_reaction_loads(R1, R2)
    assert b.reaction_loads == {R1: -13750*newton, R2: -31250*newton}

    b = Beam(3*meter, E*newton/meter**2, I*meter**4)
    b.apply_load(8*kN, 1*meter, -1)
    b.apply_load(R1, 0*meter, -1)
    b.apply_load(R2, 3*meter, -1)
    b.apply_load(12*kN*meter, 2*meter, -2)
    b.bc_deflection = [(0*meter, 0*meter), (3*meter, 0*meter)]
    b.solve_for_reaction_loads(R1, R2)
    assert b.reaction_loads == {R1: newton*Rational(-28000, 3), R2: newton*Rational(4000, 3)}
    assert b.deflection().subs(x, 1*meter) == 62000*meter/(9*E*I)

