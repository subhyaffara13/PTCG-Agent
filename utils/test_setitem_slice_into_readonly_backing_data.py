
def test_setitem_slice_into_readonly_backing_data():
    # GH#14359: test that you cannot mutate a read only buffer

    array = np.zeros(5)
    array.flags.writeable = False  # make the array immutable
    series = Series(array, copy=False)

    msg = "assignment destination is read-only"
    with pytest.raises(ValueError, match=msg):
        series[1:3] = 1

    assert not array.any()

