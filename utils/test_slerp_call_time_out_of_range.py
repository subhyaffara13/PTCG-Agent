
def test_slerp_call_time_out_of_range(xp):
    rnd = np.random.RandomState(0)
    r = Rotation.from_quat(xp.asarray(rnd.uniform(size=(5, 4))))
    t = xp.arange(5) + 1
    s = Slerp(t, r)

    times_low = xp.asarray([0, 1, 2])
    times_high = xp.asarray([1, 2, 6])
    if is_lazy_array(times_low):
        q = s(times_low).as_quat()
        in_range = xp.logical_and(times_low >= xp.min(t), times_low <= xp.max(t))
        assert xp.all(xp.isnan(q[~in_range, ...]))
        assert xp.all(~xp.isnan(q[in_range, ...]))
        q = s(times_high).as_quat()
        in_range = xp.logical_and(times_high >= xp.min(t), times_high <= xp.max(t))
        assert xp.all(xp.isnan(q[~in_range, ...]))
        assert xp.all(~xp.isnan(q[in_range, ...]))
    else:
        with pytest.raises(ValueError, match="times must be within the range"):
            s(times_low)
        with pytest.raises(ValueError, match="times must be within the range"):
            s(times_high)

