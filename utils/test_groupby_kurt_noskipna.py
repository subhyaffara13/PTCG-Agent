
def test_groupby_kurt_noskipna():
    # GH#40139
    # Test groupby.kurt() with skipna = False
    df = pd.DataFrame(
        {
            "x": [1.0, np.nan, 3.2, 4.8, 2.3, 1.9, 8.9],
            "y": [1.6, 3.3, 3.2, 6.8, 1.3, 2.9, 9.0],
        }
    )
    gb = df.groupby(by=lambda x: 0)

    result = gb.kurt(skipna=False)
    expected = pd.DataFrame({"x": [np.nan], "y": [0.1513969]})
    tm.assert_almost_equal(result, expected)

