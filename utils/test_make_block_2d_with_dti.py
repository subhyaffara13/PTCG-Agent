
def test_make_block_2d_with_dti():
    # GH#41168
    dti = pd.date_range("2012", periods=3, tz="UTC")

    msg = "make_block is deprecated"
    with tm.assert_produces_warning(Pandas4Warning, match=msg):
        blk = api.make_block(dti, placement=[0])

    assert blk.shape == (1, 3)
    assert blk.values.shape == (1, 3)

