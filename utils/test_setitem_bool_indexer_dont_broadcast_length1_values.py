
def test_setitem_bool_indexer_dont_broadcast_length1_values(size, mask, item, box):
    # GH#44265
    # see also tests.series.indexing.test_where.test_broadcast

    selection = np.resize(mask, size)

    data = np.arange(size, dtype=float)

    ser = Series(data)

    if selection.sum() != 1:
        msg = (
            "cannot set using a list-like indexer with a different "
            "length than the value"
        )
        with pytest.raises(ValueError, match=msg):
            # GH#44265
            ser[selection] = box([item])
    else:
        # In this corner case setting is equivalent to setting with the unboxed
        #  item
        ser[selection] = box([item])

        expected = Series(np.arange(size, dtype=float))
        expected[selection] = item
        tm.assert_series_equal(ser, expected)

