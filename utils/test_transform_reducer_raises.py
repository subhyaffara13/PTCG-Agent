
def test_transform_reducer_raises(all_reductions, frame_or_series, op_wrapper):
    # GH 35964
    op = op_wrapper(all_reductions)

    obj = DataFrame({"A": [1, 2, 3]})
    obj = tm.get_obj(obj, frame_or_series)

    msg = "Function did not transform"
    with pytest.raises(ValueError, match=msg):
        obj.transform(op)

