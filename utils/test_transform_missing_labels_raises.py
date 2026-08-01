
def test_transform_missing_labels_raises():
    # GH 58474
    df = DataFrame({"foo": [2, 4, 6], "bar": [1, 2, 3]}, index=["A", "B", "C"])
    msg = r"Label\(s\) \['A', 'B'\] do not exist"
    with pytest.raises(KeyError, match=msg):
        df.transform({"A": lambda x: x + 2, "B": lambda x: x * 2}, axis=0)

    msg = r"Label\(s\) \['bar', 'foo'\] do not exist"
    with pytest.raises(KeyError, match=msg):
        df.transform({"foo": lambda x: x + 2, "bar": lambda x: x * 2}, axis=1)

