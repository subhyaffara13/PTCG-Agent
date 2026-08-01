
def test_mpf_norm():
    assert mpf_norm((1, 0, 1, 0), 10) == mpf('0')._mpf_
    assert Float._new((1, 0, 1, 0), 10)._mpf_ == mpf('0')._mpf_

