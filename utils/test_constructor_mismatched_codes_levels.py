
def test_constructor_mismatched_codes_levels(idx):
    codes = [np.array([1]), np.array([2]), np.array([3])]
    levels = ["a"]

    msg = "Length of levels and codes must be the same"
    with pytest.raises(ValueError, match=msg):
        MultiIndex(levels=levels, codes=codes)

    length_error = (
        r"On level 0, code max \(3\) >= length of level \(1\)\. "
        "NOTE: this index is in an inconsistent state"
    )
    label_error = r"Unequal code lengths: \[4, 2\]"
    code_value_error = r"On level 0, code value \(-2\) < -1"

    # important to check that it's looking at the right thing.
    with pytest.raises(ValueError, match=length_error):
        MultiIndex(levels=[["a"], ["b"]], codes=[[0, 1, 2, 3], [0, 3, 4, 1]])

    with pytest.raises(ValueError, match=label_error):
        MultiIndex(levels=[["a"], ["b"]], codes=[[0, 0, 0, 0], [0, 0]])

    # external API
    with pytest.raises(ValueError, match=length_error):
        idx.copy().set_levels([["a"], ["b"]])

    with pytest.raises(ValueError, match=label_error):
        idx.copy().set_codes([[0, 0, 0, 0], [0, 0]])

    # test set_codes with verify_integrity=False
    # the setting should not raise any value error
    idx.copy().set_codes(codes=[[0, 0, 0, 0], [0, 0]], verify_integrity=False)

    # code value smaller than -1
    with pytest.raises(ValueError, match=code_value_error):
        MultiIndex(levels=[["a"], ["b"]], codes=[[0, -2], [0, 0]])

