
def test_rotation_trans_equations():
    a = CoordSys3D('a')
    from sympy.core.symbol import symbols
    q0 = symbols('q0')
    assert a._rotation_trans_equations(a._parent_rotation_matrix, a.base_scalars()) == (a.x, a.y, a.z)
    assert a._rotation_trans_equations(a._inverse_rotation_matrix(), a.base_scalars()) == (a.x, a.y, a.z)
    b = a.orient_new_axis('b', 0, -a.k)
    assert b._rotation_trans_equations(b._parent_rotation_matrix, b.base_scalars()) == (b.x, b.y, b.z)
    assert b._rotation_trans_equations(b._inverse_rotation_matrix(), b.base_scalars()) == (b.x, b.y, b.z)
    c = a.orient_new_axis('c', q0, -a.k)
    assert c._rotation_trans_equations(c._parent_rotation_matrix, c.base_scalars()) == \
           (-sin(q0) * c.y + cos(q0) * c.x, sin(q0) * c.x + cos(q0) * c.y, c.z)
    assert c._rotation_trans_equations(c._inverse_rotation_matrix(), c.base_scalars()) == \
           (sin(q0) * c.y + cos(q0) * c.x, -sin(q0) * c.x + cos(q0) * c.y, c.z)

