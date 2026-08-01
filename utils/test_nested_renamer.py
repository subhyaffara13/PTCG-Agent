
def test_nested_renamer(frame_or_series, method, func):
    # GH 35964
    obj = frame_or_series({"A": [1]})
    match = "nested renamer is not supported"
    with pytest.raises(SpecificationError, match=match):
        getattr(obj, method)(func)

