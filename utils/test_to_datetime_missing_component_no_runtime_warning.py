
def test_to_datetime_missing_component_no_runtime_warning():
    df = DataFrame(
        {
            "year": [2023, 2023],
            "month": [12, 2],
            "day": [1, 2],
            "hour": [2, np.nan],
        }
    )

    with tm.assert_produces_warning(None):
        result = to_datetime(df)

    assert result.iloc[1] is NaT

