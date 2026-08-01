
def test_groupby_kurt_all_ones():
    # GH#40139
    # Test groupby.kurt() with constant values
    df = pd.DataFrame(
        {
            "x": [1.0] * 10,
        }
    )
    gb = df.groupby(by=lambda x: 0)

    result = gb.kurt(skipna=False)
    expected = pd.DataFrame(
        {
            "x": [0.0],  # Same behavior as pd.DataFrame.kurt()
        }
    )
    tm.assert_almost_equal(result, expected)

