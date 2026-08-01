
def test_qcut_all_bins_same():
    with pytest.raises(ValueError, match="edges.*unique"):
        qcut([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 3)

