
def test_arch_member():
    a = Arch((0,0),(40,0),crown_x=20,crown_y=15)
    a.change_support_type(right_support='roller')
    a.add_member(0)
    a.apply_load(-1,'D',start=12,mag=3,angle=270)
    a.apply_load(-1,'E',start=6,mag=4,angle=270)
    a.apply_load(-1,'C',start=30,mag=5,angle=270)
    a.solve()
    assert a.reaction_force[Symbol("R_A_x")] == 0
    assert abs(a.reaction_force[Symbol("R_A_y")] - 6.750000000000000) < 10e-12
    assert a.reaction_force[Symbol("R_B_x")] == 0
    assert abs(a.reaction_force[Symbol("R_B_y")] - 5.250000000000000) < 10e-12

