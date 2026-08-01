
def test_qcut_wrong_length_labels(labels):
    # GH 13318
    values = range(10)
    msg = "Bin labels must be one fewer than the number of bin edges"
    with pytest.raises(ValueError, match=msg):
        qcut(values, 4, labels=labels)

