
def test_labels_dtypes():
    # GH 8456
    i = MultiIndex.from_tuples([("A", 1), ("A", 2)])
    assert i.codes[0].dtype == "int8"
    assert i.codes[1].dtype == "int8"

    i = MultiIndex.from_product([["a"], range(40)])
    assert i.codes[1].dtype == "int8"
    i = MultiIndex.from_product([["a"], range(400)])
    assert i.codes[1].dtype == "int16"
    i = MultiIndex.from_product([["a"], range(40000)])
    assert i.codes[1].dtype == "int32"

    i = MultiIndex.from_product([["a"], range(1000)])
    assert (i.codes[0] >= 0).all()
    assert (i.codes[1] >= 0).all()

