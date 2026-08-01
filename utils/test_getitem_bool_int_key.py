
def test_getitem_bool_int_key():
    # GH#48653
    ser = Series({True: 1, False: 0})
    with pytest.raises(KeyError, match="0"):
        ser.loc[0]

