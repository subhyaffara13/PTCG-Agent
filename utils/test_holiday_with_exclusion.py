
def test_holiday_with_exclusion():
    # GH 54382
    start = Timestamp("2020-05-01")
    end = Timestamp("2025-05-31")
    exclude = DatetimeIndex([Timestamp("2022-05-30")])  # Queen's platinum Jubilee

    queens_jubilee_uk_spring_bank_holiday = Holiday(
        "Queen's Jubilee UK Spring Bank Holiday",
        month=5,
        day=31,
        offset=DateOffset(weekday=MO(-1)),
        exclude_dates=exclude,
    )

    result = queens_jubilee_uk_spring_bank_holiday.dates(start, end)
    expected = DatetimeIndex(
        [
            Timestamp("2020-05-25"),
            Timestamp("2021-05-31"),
            Timestamp("2023-05-29"),
            Timestamp("2024-05-27"),
            Timestamp("2025-05-26"),
        ],
        dtype="datetime64[us]",
    )
    tm.assert_index_equal(result, expected)

