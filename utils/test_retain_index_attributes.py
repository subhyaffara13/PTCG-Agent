
def test_retain_index_attributes(temp_hdfstore, unit):
    # GH 3499, losing frequency info on index recreation
    dti = date_range("2000-1-1", periods=3, freq="h", unit=unit)
    df = DataFrame({"A": Series(range(3), index=dti)})

    temp_hdfstore.put("data", df, format="table")

    result = temp_hdfstore.get("data")
    tm.assert_frame_equal(df, result)

    for attr in ["freq", "tz", "name"]:
        for idx in ["index", "columns"]:
            assert getattr(getattr(df, idx), attr, None) == getattr(
                getattr(result, idx), attr, None
            )

    dti2 = date_range("2002-1-1", periods=3, freq="D", unit=unit)
    # try to append a table with a different frequency
    with tm.assert_produces_warning(errors.AttributeConflictWarning):
        df2 = DataFrame({"A": Series(range(3), index=dti2)})
        temp_hdfstore.append("data", df2)

    assert temp_hdfstore.get_storer("data").info["index"]["freq"] is None

    # this is ok
    dti3 = DatetimeIndex(
        ["2001-01-01", "2001-01-02", "2002-01-01"], dtype=f"M8[{unit}]"
    )
    df2 = DataFrame(
        {
            "A": Series(
                range(3),
                index=dti3,
            )
        }
    )
    temp_hdfstore.append("df2", df2)
    dti4 = date_range("2002-1-1", periods=3, freq="D", unit=unit)
    df3 = DataFrame({"A": Series(range(3), index=dti4)})
    temp_hdfstore.append("df2", df3)

