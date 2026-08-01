
def test_slerp_equal_times(xp):
    rnd = np.random.RandomState(0)
    q = xp.asarray(rnd.uniform(size=(5, 4)))
    r = Rotation.from_quat(q)
    t = [0, 1, 2, 2, 4]
    if is_lazy_array(q):
        s = Slerp(t, r)
        assert xp.all(xp.isnan(s.times))
    else:
        with pytest.raises(ValueError, match="strictly increasing order"):
            Slerp(t, r)

