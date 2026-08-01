
def test_setitem_bool_int_float_consistency(indexer_sli):
    # GH#21513
    # bool-with-int and bool-with-float both upcast to object
    #  int-with-float and float-with-int are both non-casting so long
    #  as the setitem can be done losslessly
    for dtype in [np.float64, np.int64]:
        ser = Series(0, index=range(3), dtype=dtype)
        with pytest.raises(TypeError, match="Invalid value"):
            indexer_sli(ser)[0] = True

        ser = Series(0, index=range(3), dtype=bool)
        with pytest.raises(TypeError, match="Invalid value"):
            ser[0] = dtype(1)

    # 1.0 can be held losslessly, so no casting
    ser = Series(0, index=range(3), dtype=np.int64)
    indexer_sli(ser)[0] = np.float64(1.0)
    assert ser.dtype == np.int64

    # 1 can be held losslessly, so no casting
    ser = Series(0, index=range(3), dtype=np.float64)
    indexer_sli(ser)[0] = np.int64(1)

