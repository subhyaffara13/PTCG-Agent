
def test_qcut_incorrect_labels(labels):
    # GH 13318
    values = range(5)
    msg = "Bin labels must either be False, None or passed in as a list-like argument"
    with pytest.raises(ValueError, match=msg):
        qcut(values, 4, labels=labels)

