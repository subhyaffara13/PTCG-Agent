
def test_error_mode_not_in_domain(method):
    # UNURAN raises an error if the mode is not in the domain
    # the behavior is different compared to the case that center is not in the
    # domain. mode is supposed to be the exact value, center can be an
    # approximate value
    Method = getattr(stats.sampling, method)
    msg = "17 : mode not in domain"
    with pytest.raises(UNURANError, match=msg):
        Method(StandardNormal(), mode=0, domain=(3, 5))

