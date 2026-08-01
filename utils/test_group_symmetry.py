
def test_group_symmetry(name, size):
    g = Rotation.create_group(name)
    q = np.concatenate((-g.as_quat(), g.as_quat()))
    distance = np.sort(cdist(q, q))
    deltas = np.max(distance, axis=0) - np.min(distance, axis=0)
    assert (deltas < TOL).all()

