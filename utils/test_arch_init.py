
def test_arch_init():
    a = Arch((0,0),(10,0),crown_x=5,crown_y=5)
    assert a.get_loads == {'distributed': {}, 'concentrated': {}}
    assert a.reaction_force == {Symbol('R_A_x'):0, Symbol('R_A_y'):0, Symbol('R_B_x'):0, Symbol('R_B_y'):0}
    assert a.supports == {'left':'hinge', 'right':'hinge'}
    assert a.left_support == (0,0)
    assert a.right_support == (10,0)
    assert a.get_shape_eqn == 5 - ((x-5)**2)/5

    a = Arch((0,0),(10,1),crown_x=6)
    a.change_support_type(left_support='roller')
    a.add_member(0.5)
    assert a.supports == {'left':'roller', 'right':'hinge'}
    assert simplify(a.get_shape_eqn) == simplify(9/5 - (x - 6)**2/20)

