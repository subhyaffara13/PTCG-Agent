
def check_named_results(res, attributes, ma=False, xp=None):
    for i, attr in enumerate(attributes):
        if ma:
            ma_npt.assert_equal(res[i], getattr(res, attr))
        elif xp is not None:
            xp_assert_equal(res[i], getattr(res, attr))
        else:
            npt.assert_equal(res[i], getattr(res, attr))

