
def test_body_add_torque():
    with warns_deprecated_sympy():
        body = Body('body')
    torque_vector = body.frame.x
    body.apply_torque(torque_vector)

    assert len(body.loads) == 1
    assert body.loads[0] == (body.frame, torque_vector)
    raises(TypeError, lambda: body.apply_torque(0))

