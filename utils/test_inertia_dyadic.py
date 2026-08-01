
def test_inertia_dyadic():
    N = ReferenceFrame('N')
    ixx, iyy, izz = symbols('ixx iyy izz')
    ixy, iyz, izx = symbols('ixy iyz izx')
    assert inertia(N, ixx, iyy, izz) == (ixx * (N.x | N.x) + iyy *
            (N.y | N.y) + izz * (N.z | N.z))
    assert inertia(N, 0, 0, 0) == 0 * (N.x | N.x)
    raises(TypeError, lambda: inertia(0, 0, 0, 0))
    assert inertia(N, ixx, iyy, izz, ixy, iyz, izx) == (ixx * (N.x | N.x) +
            ixy * (N.x | N.y) + izx * (N.x | N.z) + ixy * (N.y | N.x) + iyy *
        (N.y | N.y) + iyz * (N.y | N.z) + izx * (N.z | N.x) + iyz * (N.z |
            N.y) + izz * (N.z | N.z))

