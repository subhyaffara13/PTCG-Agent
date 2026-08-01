
def test_self_casts(dtype, dtype2, strings):
    if hasattr(dtype, "na_object"):
        strings = strings + [dtype.na_object]
    elif hasattr(dtype2, "na_object"):
        strings = strings + [""]
    arr = np.array(strings, dtype=dtype)
    newarr = arr.astype(dtype2)

    if hasattr(dtype, "na_object") and not hasattr(dtype2, "na_object"):
        assert newarr[-1] == str(dtype.na_object)
        with pytest.raises(TypeError):
            arr.astype(dtype2, casting="safe")
    elif hasattr(dtype, "na_object") and hasattr(dtype2, "na_object"):
        assert newarr[-1] is dtype2.na_object
        arr.astype(dtype2, casting="safe")
    elif hasattr(dtype2, "na_object"):
        assert newarr[-1] == ""
        arr.astype(dtype2, casting="safe")
    else:
        arr.astype(dtype2, casting="safe")

    if hasattr(dtype, "na_object") and hasattr(dtype2, "na_object"):
        na1 = dtype.na_object
        na2 = dtype2.na_object
        if (na1 is not na2 and
             # check for pd_NA first because bool(pd_NA) is an error
             ((na1 is pd_NA or na2 is pd_NA) or
              # the second check is a NaN check, spelled this way
              # to avoid errors from math.isnan and np.isnan
              (na1 != na2 and not (na1 != na1 and na2 != na2)))):
            with pytest.raises(TypeError):
                arr[:-1] == newarr[:-1]
            return
    assert_array_equal(arr[:-1], newarr[:-1])

