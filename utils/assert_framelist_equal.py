
def assert_framelist_equal(list1, list2, *args, **kwargs):
    assert len(list1) == len(list2), (
        "lists are not of equal size "
        f"len(list1) == {len(list1)}, "
        f"len(list2) == {len(list2)}"
    )
    msg = "not all list elements are DataFrames"
    both_frames = all(
        map(
            lambda x, y: isinstance(x, DataFrame) and isinstance(y, DataFrame),
            list1,
            list2,
        )
    )
    assert both_frames, msg
    for frame_i, frame_j in zip(list1, list2):
        tm.assert_frame_equal(frame_i, frame_j, *args, **kwargs)
        assert not frame_i.empty, "frames are both empty"

