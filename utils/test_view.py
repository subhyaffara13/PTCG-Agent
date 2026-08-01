
def test_view(idx):
    i_view = idx.view()
    assert_multiindex_copied(i_view, idx)

