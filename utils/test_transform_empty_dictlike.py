
def test_transform_empty_dictlike(float_frame, ops, frame_or_series):
    obj = unpack_obj(float_frame, frame_or_series, 0)

    with pytest.raises(ValueError, match="No transform functions were provided"):
        obj.transform(ops)

