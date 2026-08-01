
def test_compare_date(fixed_now_ts):
    # GH#39151 comparing NaT with date object is deprecated
    # See also: tests.scalar.timestamps.test_comparisons::test_compare_date

    dt = fixed_now_ts.to_pydatetime().date()

    msg = "Cannot compare NaT with datetime.date object"
    for left, right in [(NaT, dt), (dt, NaT)]:
        assert not left == right
        assert left != right

        with pytest.raises(TypeError, match=msg):
            left < right
        with pytest.raises(TypeError, match=msg):
            left <= right
        with pytest.raises(TypeError, match=msg):
            left > right
        with pytest.raises(TypeError, match=msg):
            left >= right

