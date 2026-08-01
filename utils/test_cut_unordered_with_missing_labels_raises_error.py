
def test_cut_unordered_with_missing_labels_raises_error():
    # GH 33141
    msg = "'labels' must be provided if 'ordered = False'"
    with pytest.raises(ValueError, match=msg):
        cut([0.5, 3], bins=[0, 1, 2], ordered=False)

