
def test_reindex_too_many_args():
    # GH 40980
    ser = Series([1, 2])
    msg = r"reindex\(\) takes from 1 to 2 positional arguments but 3 were given"
    with pytest.raises(TypeError, match=msg):
        ser.reindex([2, 3], False)

