
def test_array_impossible_casts(array, rat_cls):
    # All builtin types can be forcibly cast, at least theoretically,
    # but user dtypes cannot necessarily.
    rt = rat_cls(1, 2)
    if array:
        rt = np.array(rt)
    with assert_raises(TypeError):
        np.array(rt, dtype="M8")

