
def test_concat_mismatched_keys_length():
    # GH#43485
    ser = Series(range(5))
    sers = [ser + n for n in range(4)]
    keys = ["A", "B", "C"]

    msg = r"The length of the keys"
    with pytest.raises(ValueError, match=msg):
        concat(sers, keys=keys, axis=1)
    with pytest.raises(ValueError, match=msg):
        concat(sers, keys=keys, axis=0)
    with pytest.raises(ValueError, match=msg):
        concat((x for x in sers), keys=(y for y in keys), axis=1)
    with pytest.raises(ValueError, match=msg):
        concat((x for x in sers), keys=(y for y in keys), axis=0)

