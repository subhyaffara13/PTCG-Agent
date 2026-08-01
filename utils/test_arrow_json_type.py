
def test_arrow_json_type():
    # GH 60958
    dtype = ArrowDtype(pa.json_(pa.string()))
    result = dtype.type
    assert result == str

