
def test_transform_fastpath_raises():
    # GH#29631 case where fastpath defined in groupby.generic _choose_path
    #  raises, but slow_path does not

    df = DataFrame({"A": [1, 1, 2, 2], "B": [1, -1, 1, 2]})
    gb = df.groupby("A")

    def func(grp):
        # we want a function such that func(frame) fails but func.apply(frame)
        #  works
        if grp.ndim == 2:
            # Ensure that fast_path fails
            raise NotImplementedError("Don't cross the streams")
        return grp * 2

    # Check that the fastpath raises, see _transform_general
    obj = gb._obj_with_exclusions
    gen = gb._grouper.get_iterator(obj)
    fast_path, slow_path = gb._define_paths(func)
    _, group = next(gen)

    with pytest.raises(NotImplementedError, match="Don't cross the streams"):
        fast_path(group)

    result = gb.transform(func)

    expected = DataFrame([2, -2, 2, 4], columns=["B"])
    tm.assert_frame_equal(result, expected)

