
def test_timestamp_class_min_max_resolution():
    # when accessed on the class (as opposed to an instance), we default
    #  to nanoseconds
    assert Timestamp.min == Timestamp(NaT._value + 1)
    assert Timestamp.min._creso == NpyDatetimeUnit.NPY_FR_ns.value

    assert Timestamp.max == Timestamp(np.iinfo(np.int64).max)
    assert Timestamp.max._creso == NpyDatetimeUnit.NPY_FR_ns.value

    assert Timestamp.resolution == Timedelta(1)
    assert Timestamp.resolution._creso == NpyDatetimeUnit.NPY_FR_ns.value

