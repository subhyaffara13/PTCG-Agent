
def test_holiday_with_multiple_exclusions():
    start = Timestamp("2025-01-01")
    end = Timestamp("2065-12-31")
    exclude = DatetimeIndex(
        [
            Timestamp("2025-01-01"),
            Timestamp("2042-01-01"),
            Timestamp("2061-01-01"),
        ]
    )  # Yakudoshi new year

    yakudoshi_new_year = Holiday(
        "Yakudoshi New Year", month=1, day=1, exclude_dates=exclude
    )

    result = yakudoshi_new_year.dates(start, end)
    expected = DatetimeIndex(
        [
            Timestamp("2026-01-01"),
            Timestamp("2027-01-01"),
            Timestamp("2028-01-01"),
            Timestamp("2029-01-01"),
            Timestamp("2030-01-01"),
            Timestamp("2031-01-01"),
            Timestamp("2032-01-01"),
            Timestamp("2033-01-01"),
            Timestamp("2034-01-01"),
            Timestamp("2035-01-01"),
            Timestamp("2036-01-01"),
            Timestamp("2037-01-01"),
            Timestamp("2038-01-01"),
            Timestamp("2039-01-01"),
            Timestamp("2040-01-01"),
            Timestamp("2041-01-01"),
            Timestamp("2043-01-01"),
            Timestamp("2044-01-01"),
            Timestamp("2045-01-01"),
            Timestamp("2046-01-01"),
            Timestamp("2047-01-01"),
            Timestamp("2048-01-01"),
            Timestamp("2049-01-01"),
            Timestamp("2050-01-01"),
            Timestamp("2051-01-01"),
            Timestamp("2052-01-01"),
            Timestamp("2053-01-01"),
            Timestamp("2054-01-01"),
            Timestamp("2055-01-01"),
            Timestamp("2056-01-01"),
            Timestamp("2057-01-01"),
            Timestamp("2058-01-01"),
            Timestamp("2059-01-01"),
            Timestamp("2060-01-01"),
            Timestamp("2062-01-01"),
            Timestamp("2063-01-01"),
            Timestamp("2064-01-01"),
            Timestamp("2065-01-01"),
        ],
        dtype="datetime64[us]",
    )
    tm.assert_index_equal(result, expected)

