
def test_join_overlapping_interval_level():
    # GH 44096
    idx_1 = MultiIndex.from_tuples(
        [
            (1, Interval(0.0, 1.0)),
            (1, Interval(1.0, 2.0)),
            (1, Interval(2.0, 5.0)),
            (2, Interval(0.0, 1.0)),
            (2, Interval(1.0, 3.0)),  # interval limit is here at 3.0, not at 2.0
            (2, Interval(3.0, 5.0)),
        ],
        names=["num", "interval"],
    )

    idx_2 = MultiIndex.from_tuples(
        [
            (1, Interval(2.0, 5.0)),
            (1, Interval(0.0, 1.0)),
            (1, Interval(1.0, 2.0)),
            (2, Interval(3.0, 5.0)),
            (2, Interval(0.0, 1.0)),
            (2, Interval(1.0, 3.0)),
        ],
        names=["num", "interval"],
    )

    expected = MultiIndex.from_tuples(
        [
            (1, Interval(0.0, 1.0)),
            (1, Interval(1.0, 2.0)),
            (1, Interval(2.0, 5.0)),
            (2, Interval(0.0, 1.0)),
            (2, Interval(1.0, 3.0)),
            (2, Interval(3.0, 5.0)),
        ],
        names=["num", "interval"],
    )
    result = idx_1.join(idx_2, how="outer")

    tm.assert_index_equal(result, expected)

