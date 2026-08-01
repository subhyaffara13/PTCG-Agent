
def test_shallow_copy(idx):
    i_copy = idx._view()

    assert_multiindex_copied(i_copy, idx)

