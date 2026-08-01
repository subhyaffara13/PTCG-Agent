
def test_reindex_double_index():
    # GH 40980
    ser = Series([1, 2])
    msg = r"reindex\(\) got multiple values for argument 'index'"
    with pytest.raises(TypeError, match=msg):
        ser.reindex([2, 3], index=[3, 4])

