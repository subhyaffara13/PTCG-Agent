
def test_filter_condition_raises():
    def raise_if_sum_is_zero(x):
        if x.sum() == 0:
            raise ValueError
        return x.sum() > 0

    s = Series([-1, 0, 1, 2])
    grouper = s.apply(lambda x: x % 2)
    grouped = s.groupby(grouper)
    msg = "the filter must return a boolean result"
    with pytest.raises(TypeError, match=msg):
        grouped.filter(raise_if_sum_is_zero)

