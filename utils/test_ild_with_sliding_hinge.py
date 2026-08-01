
def test_ild_with_sliding_hinge():
    b = Beam(13, 200, 200)
    r0 = b.apply_support(0, type="pin")
    r6 = b.apply_support(6, type="pin")
    r13, m13 = b.apply_support(13, type="fixed")
    w3 = b.apply_sliding_hinge(3)
    b.solve_for_ild_reactions(1, r0, r6, r13, m13)
    a = b.ild_variable
    assert b.ild_reactions[r0].subs(a, 3) == -1
    assert b.ild_reactions[r6].subs(a, 3) == Rational(9, 14)
    assert b.ild_reactions[r13].subs(a, 9) == -Rational(207, 343)
    assert b.ild_reactions[m13].subs(a, 9) == -Rational(60, 49)
    assert b.ild_reactions[m13].subs(a, 15) == 0
    assert b.ild_reactions[m13].subs(a, -3) == 0
    assert b.ild_deflection_jumps[w3].subs(a, 9) == -Rational(9, 35000)
    b.solve_for_ild_shear(7, 1, r0, r6, r13, m13)
    assert b.ild_shear.subs(a, 8) == -Rational(200, 343)
    b.solve_for_ild_moment(8, 1, r0, r6, r13, m13)
    assert b.ild_moment.subs(a, 3) == -Rational(12, 7)

