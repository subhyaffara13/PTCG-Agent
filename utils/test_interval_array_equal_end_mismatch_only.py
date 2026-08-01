
def test_interval_array_equal_end_mismatch_only():
    arr1 = IntervalArray([Interval(0, 1), Interval(0, 5)])
    arr2 = IntervalArray([Interval(0, 1), Interval(0, 6)])

    msg = """\
IntervalArray.right are different

IntervalArray.right values are different \\(50.0 %\\)
\\[left\\]:  \\[1, 5\\]
\\[right\\]: \\[1, 6\\]"""

    with pytest.raises(AssertionError, match=msg):
        tm.assert_interval_array_equal(arr1, arr2)

