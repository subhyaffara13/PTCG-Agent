
def test_array_equivalent_dti(dtype_equal):
    assert array_equivalent(
        DatetimeIndex([0, np.nan]), DatetimeIndex([0, np.nan]), dtype_equal=dtype_equal
    )
    assert not array_equivalent(
        DatetimeIndex([0, np.nan]), DatetimeIndex([1, np.nan]), dtype_equal=dtype_equal
    )

    dti1 = DatetimeIndex([0, np.nan], tz="US/Eastern")
    dti2 = DatetimeIndex([0, np.nan], tz="CET")
    dti3 = DatetimeIndex([1, np.nan], tz="US/Eastern")

    assert array_equivalent(
        dti1,
        dti1,
        dtype_equal=dtype_equal,
    )
    assert not array_equivalent(
        dti1,
        dti3,
        dtype_equal=dtype_equal,
    )
    # The rest are not dtype_equal
    assert not array_equivalent(DatetimeIndex([0, np.nan]), dti1)
    assert array_equivalent(
        dti2,
        dti1,
    )

    assert not array_equivalent(DatetimeIndex([0, np.nan]), TimedeltaIndex([0, np.nan]))

