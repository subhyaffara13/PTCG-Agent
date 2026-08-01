
def test_transform_bad_dtype(op, frame_or_series, request):
    # GH 35964
    if op == "ngroup":
        request.applymarker(
            pytest.mark.xfail(raises=ValueError, reason="ngroup not valid for NDFrame")
        )

    obj = DataFrame({"A": 3 * [object]})  # DataFrame that will fail on most transforms
    obj = tm.get_obj(obj, frame_or_series)
    error = TypeError
    msg = "|".join(
        [
            "not supported between instances of 'type' and 'type'",
            "unsupported operand type",
        ]
    )

    with pytest.raises(error, match=msg):
        obj.transform(op)
    with pytest.raises(error, match=msg):
        obj.transform([op])
    with pytest.raises(error, match=msg):
        obj.transform({"A": op})
    with pytest.raises(error, match=msg):
        obj.transform({"A": [op]})

