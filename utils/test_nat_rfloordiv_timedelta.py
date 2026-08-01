
def test_nat_rfloordiv_timedelta(val, expected):
    # see gh-#18846
    #
    # See also test_timedelta.TestTimedeltaArithmetic.test_floordiv
    td = Timedelta(hours=3, minutes=4)
    assert td // val is expected

