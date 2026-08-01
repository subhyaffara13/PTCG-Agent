
def test_repr_max_seq_item_setting(idx):
    # GH10182
    idx = idx.repeat(50)
    with pd.option_context("display.max_seq_items", None):
        repr(idx)
        assert "..." not in str(idx)

