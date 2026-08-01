
def test_quaternion_rotation_iss1593():
    """
    There was a sign mistake in the definition,
    of the rotation matrix. This tests that particular sign mistake.
    See issue 1593 for reference.
    See wikipedia
    https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation#Quaternion-derived_rotation_matrix
    for the correct definition
    """
    q = Quaternion(cos(phi/2), sin(phi/2), 0, 0)
    assert(trigsimp(q.to_rotation_matrix()) == Matrix([
                [1,        0,         0],
                [0, cos(phi), -sin(phi)],
                [0, sin(phi),  cos(phi)]]))

