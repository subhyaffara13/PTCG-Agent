
def test_cut_read_only(array_1_writeable, array_2_writeable):
    # issue 18773
    array_1 = np.arange(0, 100, 10)
    array_1.flags.writeable = array_1_writeable

    array_2 = np.arange(0, 100, 10)
    array_2.flags.writeable = array_2_writeable

    hundred_elements = np.arange(100)
    tm.assert_categorical_equal(
        cut(hundred_elements, array_1), cut(hundred_elements, array_2)
    )

