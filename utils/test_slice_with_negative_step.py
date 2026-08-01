
def test_slice_with_negative_step(index):
    keystr1 = str(index[9])
    keystr2 = str(index[13])

    ser = Series(np.arange(20), index)
    SLC = IndexSlice

    for key in [keystr1, index[9]]:
        tm.assert_indexing_slices_equivalent(ser, SLC[key::-1], SLC[9::-1])
        tm.assert_indexing_slices_equivalent(ser, SLC[:key:-1], SLC[:8:-1])

        for key2 in [keystr2, index[13]]:
            tm.assert_indexing_slices_equivalent(ser, SLC[key2:key:-1], SLC[13:8:-1])
            tm.assert_indexing_slices_equivalent(ser, SLC[key:key2:-1], SLC[0:0:-1])

