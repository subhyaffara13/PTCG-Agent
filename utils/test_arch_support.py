
def test_arch_support():
    a = Arch((0,0),(40,0),crown_x=20,crown_y=12)
    a.apply_load(-1,'C',8,150,angle=270)
    a.apply_load(0,'D',start=20,end=40,mag=-4)
    a.solve()
    assert abs(a.reaction_force[Symbol("R_A_x")] - 83.33333333333333) < 10e-12
    assert abs(a.reaction_force[Symbol("R_B_y")] - 90.00000000000000) < 10e-12
    assert abs(a.reaction_force[Symbol("R_B_x")] + 83.33333333333333) < 10e-12
    assert abs(a.reaction_force[Symbol("R_A_y")] - 140.00000000000000) < 10e-12

