
def test_ser_tup_indexer_exceeds_dimensions(ser, keys, indexer_li):
    # GH#13831
    exp_err, exp_msg = IndexingError, "Too many indexers"
    with pytest.raises(exp_err, match=exp_msg):
        indexer_li(ser)[keys]

    if indexer_li == tm.iloc:
        # For iloc.__setitem__ we let numpy handle the error reporting.
        exp_err, exp_msg = IndexError, "too many indices for array"

    with pytest.raises(exp_err, match=exp_msg):
        indexer_li(ser)[keys] = 0

