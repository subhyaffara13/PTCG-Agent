
def test_rigidbody_default():
    # Test default
    b = RigidBody('B')
    I = inertia(b.frame, *symbols('B_ixx B_iyy B_izz B_ixy B_iyz B_izx'))
    assert b.name == 'B'
    assert b.mass == symbols('B_mass')
    assert b.masscenter.name == 'B_masscenter'
    assert b.inertia == (I, b.masscenter)
    assert b.central_inertia == I
    assert b.frame.name == 'B_frame'
    assert b.__str__() == 'B'
    assert b.__repr__() == (
        "RigidBody('B', masscenter=B_masscenter, frame=B_frame, mass=B_mass, "
        "inertia=Inertia(dyadic=B_ixx*(B_frame.x|B_frame.x) + "
        "B_ixy*(B_frame.x|B_frame.y) + B_izx*(B_frame.x|B_frame.z) + "
        "B_ixy*(B_frame.y|B_frame.x) + B_iyy*(B_frame.y|B_frame.y) + "
        "B_iyz*(B_frame.y|B_frame.z) + B_izx*(B_frame.z|B_frame.x) + "
        "B_iyz*(B_frame.z|B_frame.y) + B_izz*(B_frame.z|B_frame.z), "
        "point=B_masscenter))")

