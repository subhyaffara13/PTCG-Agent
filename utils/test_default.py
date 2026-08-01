
def test_default():
    with warns_deprecated_sympy():
        body = Body('body')
    assert body.name == 'body'
    assert body.loads == []
    point = Point('body_masscenter')
    point.set_vel(body.frame, 0)
    com = body.masscenter
    frame = body.frame
    assert com.vel(frame) == point.vel(frame)
    assert body.mass == Symbol('body_mass')
    ixx, iyy, izz = symbols('body_ixx body_iyy body_izz')
    ixy, iyz, izx = symbols('body_ixy body_iyz body_izx')
    assert body.inertia == (inertia(body.frame, ixx, iyy, izz, ixy, iyz, izx),
                            body.masscenter)

