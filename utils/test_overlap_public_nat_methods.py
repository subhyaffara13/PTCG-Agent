
def test_overlap_public_nat_methods(klass, expected):
    # see gh-17327
    #
    # NaT should have *most* of the Timestamp and Timedelta methods.
    # In case when Timestamp, Timedelta, and NaT are overlap, the overlap
    # is considered to be with Timestamp and NaT, not Timedelta.
    assert _get_overlap_public_nat_methods(klass) == expected

