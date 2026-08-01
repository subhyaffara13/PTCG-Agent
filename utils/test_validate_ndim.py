
def test_validate_ndim():
    values = np.array([1.0, 2.0])
    placement = BlockPlacement(slice(2))
    msg = r"Wrong number of dimensions. values.ndim != ndim \[1 != 2\]"

    depr_msg = "make_block is deprecated"
    with pytest.raises(ValueError, match=msg):
        with tm.assert_produces_warning(Pandas4Warning, match=depr_msg):
            make_block(values, placement, ndim=2)

