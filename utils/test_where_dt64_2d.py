
def test_where_dt64_2d():
    dti = date_range("2016-01-01", periods=6)
    dta = dti._data.reshape(3, 2)
    other = dta - dta[0, 0]

    df = DataFrame(dta, columns=["A", "B"])

    mask = np.asarray(df.isna()).copy()
    mask[:, 1] = True

    # setting part of one column, none of the other
    mask[1, 0] = True
    expected = DataFrame(
        {
            "A": np.array([other[0, 0], dta[1, 0], other[2, 0]], dtype=object),
            "B": dta[:, 1],
        }
    )
    with pytest.raises(TypeError, match="Invalid value"):
        _check_where_equivalences(df, mask, other, expected)

    # setting nothing in either column
    mask[:] = True
    expected = df
    _check_where_equivalences(df, mask, other, expected)

