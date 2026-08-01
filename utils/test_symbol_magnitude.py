
def test_symbol_magnitude():
    a = Arch((0,0),(16,0),crown_x=8,crown_y=5)
    a.apply_load(0,'C',start=3,end=5,mag=t)
    a.solve()
    assert a.reaction_force[Symbol("R_A_x")] == -(4*t)/5
    assert a.reaction_force[Symbol("R_A_y")] == -(3*t)/2
    assert a.reaction_force[Symbol("R_B_x")] == (4*t)/5
    assert a.reaction_force[Symbol("R_B_y")] == -t/2
    assert a.bending_moment_at(4) == -5*t/2

