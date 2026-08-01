
def test_log_expand_factor():
    assert (log(18)/log(3) - 2).expand(factor=True) == log(2)/log(3)
    assert (log(12)/log(2)).expand(factor=True) == log(3)/log(2) + 2
    assert (log(15)/log(3)).expand(factor=True) == 1 + log(5)/log(3)
    assert (log(2)/(-log(12) + log(24))).expand(factor=True) == 1

    assert expand_log(log(12), factor=True) == log(3) + 2*log(2)
    assert expand_log(log(21)/log(7), factor=False) == log(3)/log(7) + 1
    assert expand_log(log(45)/log(5) + log(20), factor=False) == \
        1 + 2*log(3)/log(5) + log(20)
    assert expand_log(log(45)/log(5) + log(26), factor=True) == \
        log(2) + log(13) + (log(5) + 2*log(3))/log(5)

