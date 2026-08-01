
def test_setitem_scalar_into_readonly_backing_data():
    # GH#14359: test that you cannot mutate a read only buffer

    array = np.zeros(5)
    array.flags.writeable = False  # make the array immutable
    series = Series(array, copy=False)

    for n in series.index:
        msg = "assignment destination is read-only"
        with pytest.raises(ValueError, match=msg):
            series[n] = 1

        assert array[n] == 0

