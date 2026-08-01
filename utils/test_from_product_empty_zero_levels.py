
def test_from_product_empty_zero_levels():
    # 0 levels
    msg = "Must pass non-zero number of levels/codes"
    with pytest.raises(ValueError, match=msg):
        MultiIndex.from_product([])

