
def test_map_empty(request, index):
    if isinstance(index, MultiIndex):
        request.applymarker(
            pytest.mark.xfail(
                reason="Initializing a Series from a MultiIndex is not supported"
            )
        )

    s = Series(index)
    result = s.map({})

    expected = Series(np.nan, index=s.index)
    tm.assert_series_equal(result, expected)


def test_map_empty(expected, func):
    # GH 8222
    result = expected.map(func)
    tm.assert_frame_equal(result, expected)

