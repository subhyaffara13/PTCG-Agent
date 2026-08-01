
def test_quaternion():
    # 1:
    q1 = Quaternion(1, [0, 0, 0])
    assert q1.scalar == 1
    assert (q1.vector == [0, 0, 0]).all
    # __neg__:
    assert (-q1).scalar == -1
    assert ((-q1).vector == [0, 0, 0]).all
    # i, j, k:
    qi = Quaternion(0, [1, 0, 0])
    assert qi.scalar == 0
    assert (qi.vector == [1, 0, 0]).all
    qj = Quaternion(0, [0, 1, 0])
    assert qj.scalar == 0
    assert (qj.vector == [0, 1, 0]).all
    qk = Quaternion(0, [0, 0, 1])
    assert qk.scalar == 0
    assert (qk.vector == [0, 0, 1]).all
    # i^2 = j^2 = k^2 = -1:
    assert qi*qi == -q1
    assert qj*qj == -q1
    assert qk*qk == -q1
    # identity:
    assert q1*qi == qi
    assert q1*qj == qj
    assert q1*qk == qk
    # i*j=k, j*k=i, k*i=j:
    assert qi*qj == qk
    assert qj*qk == qi
    assert qk*qi == qj
    assert qj*qi == -qk
    assert qk*qj == -qi
    assert qi*qk == -qj
    # __mul__:
    assert (Quaternion(2, [3, 4, 5]) * Quaternion(6, [7, 8, 9])
            == Quaternion(-86, [28, 48, 44]))
    # conjugate():
    for q in [q1, qi, qj, qk]:
        assert q.conjugate().scalar == q.scalar
        assert (q.conjugate().vector == -q.vector).all
        assert q.conjugate().conjugate() == q
        assert ((q*q.conjugate()).vector == 0).all
    # norm:
    q0 = Quaternion(0, [0, 0, 0])
    assert q0.norm == 0
    assert q1.norm == 1
    assert qi.norm == 1
    assert qj.norm == 1
    assert qk.norm == 1
    for q in [q0, q1, qi, qj, qk]:
        assert q.norm == (q*q.conjugate()).scalar
    # normalize():
    for q in [
        Quaternion(2, [0, 0, 0]),
        Quaternion(0, [3, 0, 0]),
        Quaternion(0, [0, 4, 0]),
        Quaternion(0, [0, 0, 5]),
        Quaternion(6, [7, 8, 9])
    ]:
        assert q.normalize().norm == 1
    # reciprocal():
    for q in [q1, qi, qj, qk]:
        assert q*q.reciprocal() == q1
        assert q.reciprocal()*q == q1
    # rotate():
    assert (qi.rotate([1, 2, 3]) == np.array([1, -2, -3])).all
    # rotate_from_to():
    for r1, r2, q in [
        ([1, 0, 0], [0, 1, 0], Quaternion(np.sqrt(1/2), [0, 0, np.sqrt(1/2)])),
        ([1, 0, 0], [0, 0, 1], Quaternion(np.sqrt(1/2), [0, -np.sqrt(1/2), 0])),
        ([1, 0, 0], [1, 0, 0], Quaternion(1, [0, 0, 0]))
    ]:
        assert Quaternion.rotate_from_to(r1, r2) == q
    # rotate_from_to(), special case:
    for r1 in [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 1]]:
        r1 = np.array(r1)
        with pytest.warns(UserWarning):
            q = Quaternion.rotate_from_to(r1, -r1)
        assert np.isclose(q.norm, 1)
        assert np.dot(q.vector, r1) == 0
    # from_cardan_angles(), as_cardan_angles():
    for elev, azim, roll in [(0, 0, 0),
                             (90, 0, 0), (0, 90, 0), (0, 0, 90),
                             (0, 30, 30), (30, 0, 30), (30, 30, 0),
                             (47, 11, -24)]:
        for mag in [1, 2]:
            q = Quaternion.from_cardan_angles(
                np.deg2rad(elev), np.deg2rad(azim), np.deg2rad(roll))
            assert np.isclose(q.norm, 1)
            q = Quaternion(mag * q.scalar, mag * q.vector)
            np.testing.assert_allclose(np.rad2deg(Quaternion.as_cardan_angles(q)),
                                       (elev, azim, roll), atol=1e-6)

