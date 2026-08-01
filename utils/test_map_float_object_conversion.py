
def test_map_float_object_conversion(val):
    # GH 2909: object conversion to float in constructor?
    df = DataFrame(data=[val, "a"])
    result = df.map(lambda x: x).dtypes[0]
    assert result == object

