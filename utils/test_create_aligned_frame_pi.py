
def test_create_aligned_frame_pi():
    N, A, P, C = _generate_body()
    f = Joint._create_aligned_interframe(P, -P.x, P.x)
    assert f.z == P.z
    f = Joint._create_aligned_interframe(P, -P.y, P.y)
    assert f.x == P.x
    f = Joint._create_aligned_interframe(P, -P.z, P.z)
    assert f.y == P.y
    f = Joint._create_aligned_interframe(P, -P.x - P.y, P.x + P.y)
    assert f.z == P.z
    f = Joint._create_aligned_interframe(P, -P.y - P.z, P.y + P.z)
    assert f.x == P.x
    f = Joint._create_aligned_interframe(P, -P.x - P.z, P.x + P.z)
    assert f.y == P.y
    f = Joint._create_aligned_interframe(P, -P.x - P.y - P.z, P.x + P.y + P.z)
    assert f.y - f.z == P.y - P.z

