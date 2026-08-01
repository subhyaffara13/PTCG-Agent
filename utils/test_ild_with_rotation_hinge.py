
def test_ild_with_rotation_hinge():
    E = Symbol('E')
    I = Symbol('I')
    F = Symbol('F')
    L1 = Symbol('L1', positive=True)
    L2 = Symbol('L2', positive=True)
    L3 = Symbol('L3', positive=True)
    b = Beam(L1 + L2 + L3, E, I)
    r0 = b.apply_support(0, type="pin")
    r1 = b.apply_support(L1 + L2, type="pin")
    r2 = b.apply_support(L1 + L2 + L3, type="pin")
    b.apply_rotation_hinge(L1 + L2)
    b.solve_for_ild_reactions(F, r0, r1, r2)
    a = b.ild_variable
    assert b.ild_reactions[r0].subs(a, 4).subs(L1, 5).subs(L2, 5).subs(L3, 10) == -3*F/5
    assert b.ild_reactions[r0].subs(a, -10).subs(L1, 5).subs(L2, 5).subs(L3, 10) == 0
    assert b.ild_reactions[r0].subs(a, 25).subs(L1, 5).subs(L2, 5).subs(L3, 10) == 0
    assert b.ild_reactions[r1].subs(a, 4).subs(L1, 5).subs(L2, 5).subs(L3, 10) == -2*F/5
    assert b.ild_reactions[r2].subs(a, 18).subs(L1, 5).subs(L2, 5).subs(L3, 10) == -4*F/5
    b.solve_for_ild_shear(L1, F, r0, r1, r2)
    assert b.ild_shear.subs(a, 7).subs(L1, 5).subs(L2, 5).subs(L3, 10) == -3*F/10
    assert b.ild_shear.subs(a, 70).subs(L1, 5).subs(L2, 5).subs(L3, 10) == 0
    b.solve_for_ild_moment(L1, F, r0, r1, r2)
    assert b.ild_moment.subs(a, 1).subs(L1, 5).subs(L2, 5).subs(L3, 10) == -F/2
    assert b.ild_moment.subs(a, 8).subs(L1, 5).subs(L2, 5).subs(L3, 10) == -F

